import frappe

def website_settings():
    settings = frappe.get_single("Website Settings")
    settings.home_page = "index"  # samaaja/www/index.html - the Vue app
    settings.banner_image = "/assets/samaaja/images/Samaaja.png"
    settings.save()
    frappe.db.commit()

def create_samaaja_settings():
    meta = frappe.get_meta("Samaaja Settings")

    def has_field(fieldname: str) -> bool:
        return bool(meta.get_field(fieldname))

    # Populate Samaaja Settings (single) with default values.
    data = {
        # Hero / leaderboard page config
        "samaaja_icon": "/assets/samaaja/images/Samaaja.png",
        "hero_bg_color": "#FFFFF5",
        "hero_text_color": "#090909",
        "tagline": "Samaaja: Where Changemakers Grow Together",
        "blurb": "#GrowWithSamaaja",
        "summary": "An open-source platform for non-profits to design, activate, and scale changemaker communities",
        "show_cta_1": 1,
        "cta1_label": "Join Samaaja",
        "cta1_link": "/discussions",
        "show_cta_2": 1,
        "cta2_label": "Join Samaaja Forum",
        "cta2_link": "/discussions",
        "show_opportunities_section_": 1,
        "show_campaign_section_": 1,

        # Leaderboard section labels
        "total_members_label": "Total Members",
        "actions_taken_label": "Actions Taken",
        "hours_invested_label": "Hours Invested",
        "verified_members_label": "Verified Members",
        "verified_members_summary": "Members who have been vetted and verified.",
        "most_active_members_label": "Most Active Members",
        "most_active_members_summary": "Top contributors who lead the change.",
        "most_active_cities_label": "Most Active Cities",
        "most_active_cities_summary": "Cities showing the greatest participation.",

        # Other settings commonly used by pages/APIs
        "location_field_name": "District",
        "user_profile_location_field": "district",

        # Child table
        "samaaja_feature_list": [
            {"feature_name": "Dynamic Portfolio", "icon": "/assets/samaaja/images/build_skills.png"},
            {"feature_name": "Leaderboards", "icon": "/assets/samaaja/images/access_mentorship.png"},
            {"feature_name": "Build Expertise", "icon": "/assets/samaaja/images/land_internships.png"},
            {"feature_name": "Funding Opportunities", "icon": "/assets/samaaja/images/seeds_funds.png"},
        ],
    }

    # Load the single doc (or create if doesn't exist — handled by frappe.get_single)
    doc = frappe.get_single("Samaaja Settings")

    # Set scalar fields (only if field exists)
    for field, value in data.items():
        if field == "samaaja_feature_list":
            continue
        if has_field(field):
            doc.set(field, value)

    # Clear and set feature list (child table)
    if has_field("samaaja_feature_list"):
        doc.set("samaaja_feature_list", [])
        for feature in data.get("samaaja_feature_list", []):
            doc.append(
                "samaaja_feature_list",
                {"feature_name": feature.get("feature_name"), "icon": feature.get("icon")},
            )

    # Save the document
    doc.save(ignore_permissions=True)
    frappe.db.commit()

def enable_energy_points():
    ss = frappe.get_single("Energy Point Settings")
    ss.enabled = 1  # the field really is called `enabled`; the old name was silently ignored
    ss.save()
    frappe.db.commit()

def after_install():
    """Runs automatically when the app is installed on a site.

    Configuration and reference data only - never demo content.
    The demo users, demo events, demo campaigns and demo opportunities that
    used to live in this file were removed deliberately. See git history if
    you ever need them back for a sales or training environment.
    """
    from samaaja.utils.temp_sync_options import sync_options

    print("Setting up Samaaja...")

    # First, because every screen after signup depends on these records:
    # signup needs the genders and user categories, Log Action needs the
    # action types and categories.
    sync_options()

    website_settings()
    create_samaaja_settings()
    enable_energy_points()

    print("Samaaja setup complete.")
