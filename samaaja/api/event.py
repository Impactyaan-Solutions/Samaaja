import json

import frappe

from samaaja.services.event import EventManager
from samaaja.utils.custom_response import custom_response

@frappe.whitelist(methods=["POST"])
def register(event):
    try:
        if frappe.session.user == "Guest":
            return custom_response(
                message="Authentication required",
                status_code=401,
            )

        return EventManager.register_for_event(
            event=event,
        ).to_custom_response()

    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            "Failed to register for event",
        )

        return custom_response(
            message="Failed to register for event",
            status_code=500,
        )

@frappe.whitelist(methods=["GET"])
def check_registered_event(event):
    try:
        if frappe.session.user == "Guest":
            return custom_response(
                message="Authentication required",
                status_code=401,
            )

        return EventManager.check_registered_event(
            event=event,
        ).to_custom_response()

    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            "Failed to check event registration",
        )

        return custom_response(
            message="Failed to check event registration",
            status_code=500,
        )
@frappe.whitelist(methods=["POST"])
def event_check_in(event):
    try:
        if frappe.session.user == "Guest":
            return custom_response(
                message="Authentication required",
                status_code=401,
            )

        return EventManager.check_in(
            event=event,
        ).to_custom_response()

    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            "Failed to check in to event",
        )

        return custom_response(
            message="Failed to check in to event",
            status_code=500,
        )