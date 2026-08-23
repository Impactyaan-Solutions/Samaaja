"""Finds addresses claimed by both Vue and Frappe."""

import frappe
from frappe.website.router import get_doctypes_with_web_view, get_pages

from samaaja.utils.spa_router import vue_config

# Frappe handles these before our routing function is ever asked, so a Vue
# screen with one of these names would simply never load. They are fixed
# strings inside frappe/app.py with no list to read from, so we name them
# here and check the assumption still holds below.
WSGI_RESERVED = {"api", "assets", "files", "private", "backups", ".well-known"}


def _assert_wsgi_assumptions():
    """Fail loudly if Frappe ever moves these, instead of silently passing."""
    import inspect

    import frappe.app

    src = inspect.getsource(frappe.app)
    for marker in ("/api/", "/backups", "/private/files/", "/.well-known/",
                   '"/assets"', '"/files"'):
        if marker not in src:
            frappe.throw(
                f"frappe/app.py no longer mentions {marker}. "
                "Review WSGI_RESERVED in samaaja/utils/route_check.py."
            )


def _ensure_request_context():
    """Give Frappe a stand-in request so its page scanner can run from the CLI.

    get_pages() calls get_base_template(page_info.route) for every www page,
    and that function starts with:

        if not path:
            path = frappe.local.request.path

    Our www/index.html serves the site root, so its route is the empty string -
    which is falsy - and Frappe reaches for the current HTTP request. In a
    `bench execute` there is no request, so it raises AttributeError.

    Only .path is ever read, so a plain dict is enough. This affects the command
    line only; during a real request frappe.local.request already exists.
    """
    try:
        frappe.local.request
    except AttributeError:
        frappe.local.request = frappe._dict(path="/")


def frappe_route_universe() -> dict[str, str]:
    """Every address Frappe could answer, and where it comes from."""
    _assert_wsgi_assumptions()
    _ensure_request_context()

    universe = {s: "framework (handled before app routing)" for s in WSGI_RESERVED}

    # Pages shipped as files by ANY installed app (frappe, eps, samaaja...)
    for route in get_pages():
        top = (route or "").strip("/").split("/")[0]
        if top:
            universe.setdefault(top, "page file in an app")

    # Route rules from any app - this is where /desk and /kb come from
    for rule in frappe.get_hooks("website_route_rules"):
        top = rule["from_route"].strip("/").split("/")[0]
        if top and not top.startswith("<"):
            universe.setdefault(top, "website_route_rules")

    # Redirects from any app - this is where /app and /apps come from
    for rule in frappe.get_hooks("website_redirects"):
        top = rule["source"].strip("/ ").split("/")[0].replace("(.*)", "").strip()
        if top:
            universe.setdefault(top, "website_redirects")

    # Anything created in the database: Web Page, Web Form, Help Article...
    for doctype in get_doctypes_with_web_view():
        try:
            for route in frappe.get_all(doctype, pluck="route"):
                top = (route or "").strip("/").split("/")[0]
                if top:
                    universe.setdefault(top, f"{doctype} record")
        except Exception:
            continue

    return universe


def check_conflicts():
    cfg = vue_config()
    vue = [r for r in cfg["routes"] if r]
    overrides = set(cfg.get("intentionalOverrides", []))

    universe = frappe_route_universe()
    clashes = [(r, universe[r]) for r in vue if r in universe and r not in overrides]

    if not clashes:
        print(f"OK - {len(vue)} Vue routes checked against "
              f"{len(universe)} Frappe routes, no conflicts")
        return

    print(f"\nFOUND {len(clashes)} ROUTE CONFLICT(S):\n")
    for slug, source in clashes:
        print(f"   /{slug}   is also served by: {source}")
    print("\nEither rename the Vue route, or add it to intentionalOverrides "
          "in frontend/vite.config.js if you meant to take it over.\n")
    raise frappe.ValidationError(f"{len(clashes)} route conflict(s)")


def validate_route_not_claimed(doc, method=None):
    """Stops someone creating a Web Page at an address Vue already uses."""
    if not doc.route:
        return
    top = doc.route.strip("/").split("/")[0]
    if top in set(vue_config()["routes"]):
        frappe.throw(
            f"Route '/{doc.route}' clashes with the Samaaja app. "
            f"'/{top}' is served by the frontend, so this page would never be seen."
        )
