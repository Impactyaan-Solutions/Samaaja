import frappe

from samaaja.utils.theme import get_theme_css

no_cache = 1


def get_context(context):
    # Branding colours and custom CSS from Samaaja Settings, rendered into
    # the <style id="samaaja-theme"> tag that vite.config.js adds to
    # www/index.html. The rest of the app fetches its data through the API.
    try:
        context.theme_css = get_theme_css()
    except Exception:
        # Never block the app over branding: fall back to the defaults in style.css.
        frappe.log_error(frappe.get_traceback(), "Failed to build theme CSS")
        context.theme_css = ""
