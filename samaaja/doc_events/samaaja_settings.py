import frappe
from frappe.utils.password import get_decrypted_password


def validate(doc, method):
    if doc.enable_otp_login and not _sms_is_configured():
        frappe.throw(
            "OTP login needs SMS to be configured first. Set it up in "
            "SMS Settings before enabling this."
        )

    if doc.enable_google_login and not _google_key_is_configured():
        frappe.throw(
            "Google login needs a Social Login Key for Google with a "
            "Client ID and Client Secret saved before enabling this."
        )

    if not doc.enable_phone_login:
        # OTP is a mode of phone login, not a standalone method - leaving it
        # set while phone login itself is off would be a stale, meaningless
        # combination sitting in the data.
        doc.enable_otp_login = 0

        # Exclude Google from this DB check - its enable_social_login flag
        # hasn't been synced to match doc.enable_google_login yet (that
        # happens below), so checking it here would read stale pre-save
        # state. doc.enable_google_login already tells us Google's real
        # post-save state directly.
        if not doc.enable_google_login and not _has_enabled_social_login(excluding_name="google"):
            frappe.throw(
                "At least one sign-in method must stay enabled. Enable "
                "phone number login, or enable Google login, before "
                "turning this off."
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
    if frappe.get_single("Samaaja Settings").enable_phone_login:
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
