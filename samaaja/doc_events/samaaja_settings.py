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


def _has_enabled_social_login():
    providers = frappe.get_all(
        "Social Login Key",
        filters={"enable_social_login": 1},
        fields=["name"],
    )
    for provider in providers:
        if get_decrypted_password(
            "Social Login Key", provider.name, "client_secret", raise_exception=False
        ):
            return True
    return False
