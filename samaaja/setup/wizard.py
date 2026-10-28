import frappe

def get_setup_stages(args=None):
    return [{
        "status": "Setting up your branding",
        "fail_msg": "Could not save branding settings",
        "tasks": [{
            "fn": configure_branding,
            "args": args,
            "fail_msg": "Could not save branding settings",
        }],
    }]

def configure_branding(args):
    args = frappe._dict(args or {})

    settings = frappe.get_single("Samaaja Settings")
    settings.app_logo = args.get("app_logo") or settings.app_logo
    settings.app_name = args.get("app_name") or settings.app_name or "Samaaja"
    settings.tagline = args.get("tagline") or settings.tagline
    settings.primary_color = args.get("primary_color") or settings.primary_color
    settings.accent_color = args.get("accent_color") or settings.accent_color
    settings.save(ignore_permissions=True)
