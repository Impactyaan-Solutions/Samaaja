import frappe

from samaaja.services.branding import BrandingManager
from samaaja.utils.custom_response import custom_response


@frappe.whitelist(methods=["GET"], allow_guest=True)
def get_branding():
    # Guest access: the login and landing pages show the name and logo.
    try:
        return BrandingManager.get_branding().to_custom_response()

    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            "Failed to fetch branding"
        )

        return custom_response(
            message="Failed to fetch branding",
            status_code=500
        )
