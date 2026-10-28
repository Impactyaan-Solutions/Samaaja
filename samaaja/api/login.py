import frappe
from frappe.utils.oauth import get_oauth2_authorize_url, get_oauth_keys
from frappe.utils.password import get_decrypted_password
from samaaja.services.user import UserManager
from samaaja.utils.custom_response import custom_response

@frappe.whitelist(allow_guest=True)
def get_login_options():
    """
    What the login screen should actually show: whether phone number login
    is enabled at all, whether OTP replaces password when it is, and which
    social providers are both gated on in Samaaja Settings and actually
    configured. Uses frappe.get_single() rather than a raw DB read so a
    newly added setting still resolves to its schema default on sites that
    haven't saved Samaaja Settings since the field was added.
    """
    settings = frappe.get_single("Samaaja Settings")
    return {
        "phone_login_enabled": bool(settings.enable_phone_login),
        "otp_enabled": bool(settings.enable_otp_login),
        "providers": _get_social_providers(settings),
    }

def _get_social_providers(settings):
    # No hardcoded provider list here - a provider is offered only if BOTH
    # of these are true, checked directly against the live doctypes:
    #   1. A real "Social Login Key" record exists with that exact name
    #      (so this can never drift from what Frappe itself knows about).
    #   2. Samaaja Settings has a Check field named enable_<key-name>_login
    #      that's turned on. The field is looked up by name through the
    #      doctype's own meta, not assumed to exist, so a Social Login Key
    #      with no matching Settings field is just silently skipped.
    # To offer a new provider later: create its Social Login Key record,
    # add one enable_<name>_login Check field to Samaaja Settings, and a
    # guard in doc_events/samaaja_settings.py mirroring enable_google_login
    # there. Nothing in this file needs to change.
    meta = frappe.get_meta("Samaaja Settings")
    result = []

    for key_name in frappe.get_all("Social Login Key", pluck="name"):
        settings_field = f"enable_{key_name}_login"
        if not meta.get_field(settings_field):
            continue
        if not settings.get(settings_field):
            continue

        provider = _get_configured_provider(key_name)
        if provider:
            result.append(provider)

    return result

def _get_configured_provider(name):
    if not frappe.db.exists("Social Login Key", name):
        return None

    provider = frappe.db.get_value(
        "Social Login Key",
        name,
        ["name", "client_id", "base_url", "provider_name", "icon", "enable_social_login"],
        as_dict=True,
    )
    if not provider.enable_social_login:
        return None

    client_secret = get_decrypted_password(
        "Social Login Key", provider.name, "client_secret", raise_exception=False
    )
    if not client_secret:
        return None

    if not (provider.client_id and provider.base_url and get_oauth_keys(provider.name)):
        return None

    return {
        "name": provider.name,
        "provider_name": provider.provider_name,
        "icon": provider.icon,
        "auth_url": get_oauth2_authorize_url(provider.name, redirect_to="/homepage"),
    }

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
