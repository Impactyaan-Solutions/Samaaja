import frappe

def website_settings():
    settings = frappe.get_single("Website Settings")
    settings.home_page = "index"  # samaaja/www/index.html - the Vue app
    settings.banner_image = "/assets/samaaja/images/Samaaja.png"
    settings.save()
    frappe.db.commit()

def create_samaaja_settings():
    # Samaaja Settings has no scalar fields left to seed with defaults
    # (Authentication's own fields already default correctly from the
    # doctype schema) - this just makes sure the single actually gets
    # saved as a real record at install time.
    frappe.get_single("Samaaja Settings").save(ignore_permissions=True)
    frappe.db.commit()

def enable_energy_points():
    ss = frappe.get_single("Energy Point Settings")
    ss.enabled = 1  # the field really is called `enabled`; the old name was silently ignored
    ss.save()
    frappe.db.commit()

# Reference data the app's dropdowns depend on. Without these, a fresh site
# breaks in three places: signup fails on gender, profile completion fails
# on category, and logging an action fails on both type and category. Most
# of the app now reads these values through the metadata API (see
# samaaja.services.metadata) instead of hardcoding them in Vue, and they're
# editable afterward from Samaaja Settings' Metadata tab - this is just the
# one-time seed so a fresh site isn't empty.
#
# Additive only: it never renames or deletes, because existing Action and
# User Metadata records may point at values no longer offered.
REFERENCE_OPTIONS = {
    "Gender": {
        "field": "gender",
        "defaults": {},
        "values": ["Male", "Female", "Transgender", "Others", "Prefer not to say"],
    },
    "User Category": {
        "field": "category_name",
        "defaults": {"is_active": 1},
        "values": ["Citizen", "NGO Partner"],
    },
    "Action Type": {
        "field": "type",
        "defaults": {},
        "values": [
            "On-Ground Action",
            "Data & Reporting",
            "Training & Mentoring",
            "Events & Activities",
            "Outreach & Awareness",
            "Community Engagement",
        ],
    },
    "Action Category": {
        "field": "category",
        "defaults": {},
        "values": [
            "Agriculture & Livelihood",
            "Health & Nutrition",
            "Education",
            "Civic Action & Governance",
            "Sports & Fitness",
        ],
    },
}

def seed_reference_options():
    """Create any missing reference records. Safe to run repeatedly."""
    created = []

    for doctype, cfg in REFERENCE_OPTIONS.items():
        field = cfg["field"]
        defaults = cfg.get("defaults") or {}

        for value in cfg["values"]:
            if frappe.db.exists(doctype, {field: value}):
                continue
            doc = frappe.new_doc(doctype)
            doc.set(field, value)
            for key, val in defaults.items():
                doc.set(key, val)
            doc.insert(ignore_permissions=True, ignore_if_duplicate=True)
            created.append(f"{doctype}: {value}")

    if created:
        print(f"Created {len(created)} option record(s):")
        for line in created:
            print("  ", line)
    else:
        print("All dropdown options already present.")

def report_orphans():
    """List reference records in Frappe that the app no longer offers.

    Read-only. Worth running before a release to see which values users may
    have selected in the past but can no longer choose.
    """
    for doctype, cfg in REFERENCE_OPTIONS.items():
        field = cfg["field"]
        wanted = set(cfg["values"])
        existing = set(frappe.get_all(doctype, pluck=field))
        extra = existing - wanted
        if extra:
            print(f"{doctype}: {len(extra)} not offered by the app")
            for value in sorted(extra):
                print("   ", value)

# Default badges and the Energy Point Rules that award them, copied from an
# existing deployment that already had these configured by hand. Each rule
# awards 10 points once per matching Action (apply_only_once=1) and ties to
# the badge of the same name via the custom "badge" field this app adds to
# Energy Point Rule (see samaaja/samaaja/custom/energy_point_rule.json).
BADGES_AND_POINTS = [
    {
        "title": "Agri Hero",
        "icon": "agri-hero.png",
        "rule_name": "Agri Hero Rule",
        "condition": 'doc.type == "Events & Activities" and doc.category == "Agriculture & Livelihood"',
    },
    {
        "title": "Community Leader",
        "icon": "community-leader.png",
        "rule_name": "Community Leader Rule",
        "condition": 'doc.type == "Community Engagement" and doc.category == "Health & Nutrition"',
    },
    {
        "title": "Sports Catalyst",
        "icon": "sports-catalyst.jpeg",
        "rule_name": "Sports Catalyst Rule",
        "condition": 'doc.type == "On-Ground Action" and doc.category == "Sports & Fitness"',
    },
    {
        "title": "Green Warrior",
        "icon": "green-warrior.jpg",
        "rule_name": "Green Warrior Rule",
        "condition": 'doc.type == "Outreach & Awareness" and doc.category == "Civic Action & Governance"',
    },
    {
        "title": "Shiksha Champion",
        "icon": "shiksha-champion.png",
        "rule_name": "Shiksha Champion Rule",
        "condition": 'doc.type == "Training & Mentoring" and doc.category == "Education"',
    },
    {
        "title": "People Supporter",
        "icon": "people-supporter.png",
        "rule_name": "People Supporter Rule",
        "condition": 'doc.type == "Events & Activities"',
    },
    {
        "title": "Community Builder",
        "icon": "community-builder.webp",
        "rule_name": "Community Builder Rule",
        "condition": 'doc.type == "Community Engagement"',
    },
    {
        "title": "Active Champion",
        "icon": "active-champion.jpg",
        "rule_name": "Active Champion Rule",
        "condition": 'doc.type == "On-Ground Action"',
    },
    {
        "title": "Awareness Driver",
        "icon": "awareness-driver.avif",
        "rule_name": "Awareness Driver Rule",
        "condition": 'doc.type == "Outreach & Awareness"',
    },
    {
        "title": "Knowledge Sharer",
        "icon": "knowledge-sharer.jpg",
        "rule_name": "Knowledge Sharer Rule",
        "condition": 'doc.type == "Training & Mentoring"',
    },
    {
        "title": "Data Champion",
        "icon": "data-champion.png",
        "rule_name": "Data Champion Rule",
        "condition": 'doc.type == "Data & Reporting"',
    },
]

def seed_badges_and_points():
    """Create any missing badges and their Energy Point Rules. Safe to run
    repeatedly - matches on Badge title and Energy Point Rule rule_name.
    """
    created = []

    for entry in BADGES_AND_POINTS:
        if not frappe.db.exists("Badge", entry["title"]):
            frappe.get_doc({
                "doctype": "Badge",
                "title": entry["title"],
                "icon": f"/assets/samaaja/images/badges/{entry['icon']}",
            }).insert(ignore_permissions=True)
            created.append(f"Badge: {entry['title']}")

        if not frappe.db.exists("Energy Point Rule", {"rule_name": entry["rule_name"]}):
            frappe.get_doc({
                "doctype": "Energy Point Rule",
                "rule_name": entry["rule_name"],
                "enabled": 1,
                "reference_doctype": "Action",
                "for_doc_event": "Custom",
                "points": 10,
                "for_assigned_users": 0,
                "user_field": "user",
                "max_points": 0,
                "apply_only_once": 1,
                "condition": entry["condition"],
                "badge": entry["title"],
            }).insert(ignore_permissions=True)
            created.append(f"Energy Point Rule: {entry['rule_name']}")

    if created:
        print(f"Created {len(created)} badge/point record(s):")
        for line in created:
            print("  ", line)
    else:
        print("All badges and point rules already present.")

def after_install():
    """Runs automatically when the app is installed on a site.

    Configuration and reference data only - never demo content.
    The demo users, demo events, demo campaigns and demo opportunities that
    used to live in this file were removed deliberately. See git history if
    you ever need them back for a sales or training environment.
    """
    print("Setting up Samaaja...")
    # First, because every screen after signup depends on these records:
    # signup needs the genders and user categories, Log Action needs the
    # action types and categories.
    seed_reference_options()
    website_settings()
    create_samaaja_settings()
    enable_energy_points()
    seed_badges_and_points()
    print("Samaaja setup complete.")
