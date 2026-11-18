import frappe
from frappe.utils.password import get_decrypted_password


def validate(doc, method):
    frappe.log_error(
    title="Login Validation Debug",
    message=f"""
    Email Login: {doc.enable_email_login}
    OTP Login: {doc.enable_otp_login}
    Google Login: {doc.enable_google_login}
    SMS Configured: {_sms_is_configured()}
    """
    )
    if not frappe.conf.get("enable_custom_login_feature", 0):

        if doc.enable_email_login:

            if not _email_is_configured():
                frappe.throw(
                    "Cannot enable Email Login. Please configure and enable "
                    "at least one outgoing Email Account first."
                )
                
    if doc.enable_otp_login and not _sms_is_configured():
        frappe.throw(
           "Cannot enable OTP login. Please configure SMS Settings first."
        )

    if doc.enable_google_login and not _google_key_is_configured():
        frappe.throw(
            "Cannot enable Google Login. Please configure Google"
            "Social Login Key with Client ID and Client Secret first."
        )

    

    # Samaaja Settings is now the real switch the frontend reads - keep the
    # Social Login Key's own flag in sync so core's OAuth callback (which
    # checks that flag independently) doesn't reject a login this toggle
    # says is on, or accept one it says is off.
    _sync_google_social_login_key(enabled=bool(doc.enable_google_login))


def validate_social_login_key(doc, method):
    """Same invariant as validate() above, checked from the other
    direction: a Social Login Key being disabled or its secret cleared.
    """
    if _is_enabled_with_secret(doc):
        return
    _guard_last_sign_in_method(doc.name)
    _clear_google_toggle_if_this_key(doc.name)


def on_trash_social_login_key(doc, method):
    _guard_last_sign_in_method(doc.name)
    _clear_google_toggle_if_this_key(doc.name)


def _guard_last_sign_in_method(excluding_name):
    if frappe.get_single("Samaaja Settings").enable_email_login:
        return

    if not _has_enabled_social_login(excluding_name=excluding_name):
        frappe.throw(
            "At least one sign-in method must stay enabled. Enable phone "
            "number login in Samaaja Settings before disabling or deleting "
            "the last configured Social Login Key."
        )


def _clear_google_toggle_if_this_key(name):
    # Disabling/deleting the Google key directly (outside Samaaja Settings)
    # would otherwise leave the Settings toggle stuck "on" pointing at
    # nothing - same stale-state problem fixed for OTP above.
    if name != "google":
        return
    frappe.db.set_single_value("Samaaja Settings", "enable_google_login", 0)


def _is_enabled_with_secret(doc):
    if not doc.enable_social_login:
        return False
    return bool(doc.get_password("client_secret", raise_exception=False))


def _has_enabled_social_login(excluding_name=None):
    filters = {"enable_social_login": 1}
    if excluding_name:
        filters["name"] = ["!=", excluding_name]

    providers = frappe.get_all(
        "Social Login Key",
        filters=filters,
        fields=["name"],
    )
    for provider in providers:
        if get_decrypted_password(
            "Social Login Key", provider.name, "client_secret", raise_exception=False
        ):
            return True
    return False


def _sms_is_configured():
    return bool(frappe.db.get_single_value("SMS Settings", "sms_gateway_url"))

def _email_is_configured():
    return bool(
        frappe.db.exists(
            "Email Account",
            {
                "enable_outgoing": 1,
                "email_id": ["is", "set"]
            }
        )
    )
def _google_key_is_configured():
    if not frappe.db.exists("Social Login Key", "google"):
        return False
    client_id = frappe.db.get_value("Social Login Key", "google", "client_id")
    client_secret = get_decrypted_password(
        "Social Login Key", "google", "client_secret", raise_exception=False
    )
    return bool(client_id) and bool(client_secret)


def _sync_google_social_login_key(enabled):
    if not frappe.db.exists("Social Login Key", "google"):
        return
    frappe.db.set_value(
        "Social Login Key", "google", "enable_social_login", 1 if enabled else 0
    )
