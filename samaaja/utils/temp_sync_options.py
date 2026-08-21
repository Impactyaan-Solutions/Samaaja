"""TEMPORARY: creates the reference records the app's dropdowns depend on.

Without these, a fresh site breaks in three places: signup fails on gender,
profile completion fails on category, and logging an action fails on both
type and category. They were never created by any code -- the live site
only has them because somebody set them up by hand long ago.

TEMPORARY ARRANGEMENT
---------------------
The values below are ALSO hardcoded into four Vue screens:

    frontend/src/views/LogAction.vue          (action type, action category)
    frontend/src/views/AddPost.vue            (action category)
    frontend/src/views/ProfileCompletion.vue  (gender, user category)
    frontend/src/views/Signup.vue             (gender, user category)

Nothing keeps the two copies in step. Add a choice here and it will not
appear in the dropdown. Add it to a screen without adding it here and
saving fails with "Could not find Action Type: ...".

The proper fix is to serve these lists from the API so there is only one
copy and an admin can edit them in Frappe. Tracked as SAM-18. When that
lands, this whole file goes away.

Additive only: it never renames or deletes, because existing Action and
User Metadata records may point at values no longer offered.
"""

import frappe

# doctype -> how to create its records
#   field    : the field the value goes into (records are matched on it)
#   defaults : any other field to set when creating
#   values   : the choices, exactly as the Vue screens send them
OPTIONS = {
    "Gender": {
        "field": "gender",
        "defaults": {},
        "values": ["Male", "Female", "Other"],
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


def sync_options():
    """Create any missing records. Safe to run repeatedly."""
    created = []

    for doctype, cfg in OPTIONS.items():
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
    """List records in Frappe that the app no longer offers.

    Read-only. Worth running before a release to see which values users may
    have selected in the past but can no longer choose.
    """
    for doctype, cfg in OPTIONS.items():
        field = cfg["field"]
        wanted = set(cfg["values"])
        existing = set(frappe.get_all(doctype, pluck=field))
        extra = existing - wanted
        if extra:
            print(f"{doctype}: {len(extra)} not offered by the app")
            for value in sorted(extra):
                print("   ", value)
