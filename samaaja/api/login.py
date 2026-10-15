import frappe
from frappe.utils.oauth import get_oauth2_authorize_url, get_oauth_keys
from frappe.utils.password import get_decrypted_password
from samaaja.services.user import UserManager
from samaaja.utils.custom_response import custom_response

@frappe.whitelist(allow_guest=True)
def get_login_options():
    """
    What the login screen should actually show, instead of assuming Google:
    every enabled Social Login Key with a usable secret, plus whether OTP
    login is turned on (samaaja_settings.enable_otp_login).
    """
    return {
        "otp_enabled": bool(frappe.db.get_single_value("Samaaja Settings", "enable_otp_login")),
        "providers": _get_social_providers(),
    }

def _get_social_providers():
    # Mirrors frappe/www/login.py's own provider-listing logic.
    providers = frappe.get_all(
        "Social Login Key",
        filters={"enable_social_login": 1},
        fields=["name", "client_id", "base_url", "provider_name", "icon"],
        order_by="name",
    )

    result = []
    for provider in providers:
        client_secret = get_decrypted_password(
            "Social Login Key", provider.name, "client_secret", raise_exception=False
        )
        if not client_secret:
            continue

        if provider.client_id and provider.base_url and get_oauth_keys(provider.name):
            result.append({
                "name": provider.name,
                "provider_name": provider.provider_name,
                "icon": provider.icon,
                "auth_url": get_oauth2_authorize_url(provider.name, redirect_to="/homepage"),
            })

    return result

@frappe.whitelist(allow_guest=True)
def login_using_otp(mobile_no:str,otp:str):
    try:
        return UserManager.login_using_OTP(mobile_no, otp).to_custom_response()
    except Exception as e:
        frappe.log_error(
            frappe.get_traceback(),
            "Failed to log in user"
        )
        return custom_response(status_code=500, message="Internal Server Error")

@frappe.whitelist(allow_guest=True)
def login_using_password(mobile_no:str,password:str):
    try:
        return UserManager.login_using_password(mobile_no, password).to_custom_response()
    except Exception as e:
        frappe.log_error(
            frappe.get_traceback(),
            "Failed to log in user"
        )
        return custom_response(status_code=500, message="Internal Server Error")
