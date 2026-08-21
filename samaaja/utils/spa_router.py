"""Decides, for each request, whether Vue or Frappe should answer."""

import json
import os

import frappe
import werkzeug.routing.exceptions
from frappe.website.page_renderers.document_page import DocumentPage
from frappe.website.page_renderers.list_renderer import ListPage
from frappe.website.page_renderers.print_page import PrintPage
from frappe.website.page_renderers.static_page import StaticPage
from frappe.website.page_renderers.template_page import TemplatePage
from frappe.website.page_renderers.web_form import WebFormPage
from frappe.website.path_resolver import PathResolver, resolve_path

RENDERERS = (StaticPage, WebFormPage, DocumentPage, TemplatePage, PrintPage, ListPage)


def vue_config():
    """The route list written by the frontend build."""
    path = os.path.join(frappe.get_app_path("samaaja"), "vue_routes.json")
    if not os.path.exists(path):
        frappe.throw(
            "vue_routes.json is missing. Run `bench build --app samaaja` "
            "before starting the site."
        )
    with open(path) as f:
        return json.load(f)


def vue_routes():
    return set(frappe.cache.get_value(
        "samaaja_vue_routes", lambda: vue_config()["routes"]
    ))


def resolve_spa_path(path):
    top = path.strip("/ ").split("/")[0]

    # 1. Vue's own screens always win.
    if top in vue_routes():
        return "index"

    # 2. Let Frappe work out what this address means.
    try:
        endpoint = resolve_path(path)
    except werkzeug.routing.exceptions.RequestRedirect:
        return "index"

    # 3. Does Frappe actually have a real page here?
    for renderer_cls in (*PathResolver.get_custom_page_renderers(), *RENDERERS):
        if renderer_cls(endpoint, None).can_render():
            return endpoint

    # 4. Nobody has this address - show Vue's "not found" screen.
    return "index"
