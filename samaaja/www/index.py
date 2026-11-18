import frappe

no_cache = 1


def get_context(context):
    settings = frappe.get_single("Samaaja Settings")
    context.app_colour = settings.colour or "#2563eb"  # fallback to default blue
