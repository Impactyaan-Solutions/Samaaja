import frappe


@frappe.whitelist(allow_guest=True)
def get_branding():
    """What the login/signup/landing screens should show for identity:
    app name, logo, tagline, and brand colors. Guest-callable and separate
    from get_login_options() since the Landing page needs this regardless
    of login state.
    """
    settings = frappe.get_single("Samaaja Settings")
    return {
        "app_name": settings.app_name or "Samaaja",
        "logo": settings.app_logo or None,
        "tagline": settings.tagline or None,
        "primary_color": settings.primary_color or None,
        "accent_color": settings.accent_color or None,
    }
