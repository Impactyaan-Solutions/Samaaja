import frappe

PROVIDERS = ["Google", "Facebook"]

def get_setup_stages(args=None):
    return [{
        "status": "Setting up Samaaja authentication",
        "fail_msg": "Could not complete Samaaja authentication setup",
        "tasks": [{
            "fn": configure_authentication,
            "args": args,
            "fail_msg": "Could not save authentication settings",
        }],
    }]

def configure_authentication(args):
    args = frappe._dict(args or {})

    # Social keys first: if the admin is disabling phone login in this same
    # submission, Samaaja Settings' own validation (at least one sign-in
    # method must stay enabled) needs to see what was just configured.
    for provider in PROVIDERS:
        key = frappe.scrub(provider)
        if not args.get(f"enable_{key}"):
            continue

        client_id = args.get(f"{key}_client_id")
        client_secret = args.get(f"{key}_client_secret")
        if not client_id or not client_secret:
            continue

        _enable_social_login_key(provider, client_id, client_secret)

    settings = frappe.get_single("Samaaja Settings")
    settings.enable_phone_login = 1 if args.get("enable_phone_login", 1) else 0
    settings.enable_otp_login = 1 if args.get("enable_otp_login") else 0
    settings.save(ignore_permissions=True)

def _enable_social_login_key(provider, client_id, client_secret):
    name = frappe.scrub(provider)
    if frappe.db.exists("Social Login Key", name):
        doc = frappe.get_doc("Social Login Key", name)
    else:
        doc = frappe.new_doc("Social Login Key")
        doc.provider_name = provider
        doc.social_login_provider = provider
        # Same lookup the desk form uses when you pick a provider from the
        # dropdown - fills in the correct authorize/access-token/redirect
        # URLs instead of us hardcoding them here.
        doc.update(doc.get_social_login_provider(provider))

    doc.client_id = client_id
    doc.client_secret = client_secret
    doc.enable_social_login = 1
    doc.save(ignore_permissions=True)
