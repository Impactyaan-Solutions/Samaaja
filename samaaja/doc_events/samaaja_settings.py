import frappe
from frappe.utils.password import get_decrypted_password


def validate(doc, method):
    """At least one way to sign in must stay enabled - phone login, or a
    fully configured (enabled + has a usable secret) social provider.
    """
    if doc.enable_phone_login:
        return

    # OTP is a mode of phone login, not a standalone method - leaving it
    # set while phone login itself is off would be a stale, meaningless
    # combination sitting in the data (the UI already hides the checkbox
    # in this state, but that alone doesn't clear a previously-saved value).
    doc.enable_otp_login = 0

    if not _has_enabled_social_login():
        frappe.throw(
            "At least one sign-in method must stay enabled. Enable phone "
            "number login, or configure and enable a Social Login Key, "
            "before turning this off."
        )


def validate_social_login_key(doc, method):
    """Same invariant as validate() above, checked from the other
    direction: a Social Login Key being disabled or its secret cleared.
    """
    if _is_enabled_with_secret(doc):
        return
    _guard_last_sign_in_method(doc.name)


def on_trash_social_login_key(doc, method):
    _guard_last_sign_in_method(doc.name)


def _guard_last_sign_in_method(excluding_name):
    if frappe.get_single("Samaaja Settings").enable_phone_login:
        return

    if not _has_enabled_social_login(excluding_name=excluding_name):
        frappe.throw(
            "At least one sign-in method must stay enabled. Enable phone "
            "number login in Samaaja Settings before disabling or deleting "
            "the last configured Social Login Key."
        )


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
