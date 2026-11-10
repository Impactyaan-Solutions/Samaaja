from . import __version__ as app_version

app_name = "samaaja"
app_title = "Samaaja"
app_publisher = "Impactyaan"
app_description = "Samaaja is an open source software solution for rapidly building location based civic services connected with volunteer, human interactions. It comes with all necessary UI and management features and can be easily extended into web applications and external mobile apps and systems via built-in APIs."
app_email = "ankit@impactyaan.com"
app_license = "MIT"

# Energy Points was removed from Frappe core in v16 and lives in its own app.
# Samaaja adds custom fields onto Energy Point records, so `eps` must already
# be installed before this app is. Listing it here makes bench do that for us.
required_apps = ["eps"]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/samaaja/css/samaaja.css"
# app_include_js = "/assets/samaaja/js/samaaja.js"

# include js, css files in header of web template
web_include_css = ["samaaja.bundle.css"]
web_include_js = ""

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "samaaja/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "samaaja.utils.jinja_methods",
# 	"filters": "samaaja.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "samaaja.install.before_install"

# Runs once, right after `bench install-app samaaja`. Creates the settings,
# website configuration and reference records the app cannot work without.
after_install = "samaaja.setup.samaaja_setup.after_install"

# Runs on every `bench migrate`, i.e. on every deploy. Only creates dropdown
# records that are missing, so it is cheap and safe to repeat. This is why it
# can live here while the old setup_samaaja (which also seeded demo users and
# crashed on missing doctypes) had to stay commented out.
after_migrate = "samaaja.setup.samaaja_setup.seed_reference_options"

# See samaaja/public/js/setup_wizard.js and samaaja/setup/wizard.py.
setup_wizard_requires = "assets/samaaja/js/setup_wizard.js"
setup_wizard_stages = "samaaja.setup.wizard.get_setup_stages"

# Uninstallation
# ------------

# before_uninstall = "samaaja.uninstall.before_uninstall"
# after_uninstall = "samaaja.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "samaaja.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"samaaja.tasks.all"
# 	],
# 	"daily": [
# 		"samaaja.tasks.daily"
# 	],
# 	"hourly": [
# 		"samaaja.tasks.hourly"
# 	],
# 	"weekly": [
# 		"samaaja.tasks.weekly"
# 	],
# 	"monthly": [
# 		"samaaja.tasks.monthly"
# 	],
# }

scheduler_events = {
    #"all": ["samaaja.tasks.location_update"],
    # "hourly": ["samaaja.tasks.badge_update"]
}


# Testing
# -------

# before_tests = "samaaja.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "samaaja.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "samaaja.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"samaaja.auth.validate"
# ]

# Decides, for every incoming address, whether the Vue app or Frappe answers.
# Frappe has no resolver of its own, so ours simply takes over. See
# samaaja/utils/spa_router.py for the rules it applies.
website_path_resolver = ["samaaja.utils.spa_router.resolve_spa_path"]

# Removed with the legacy Jinja pages:
#   page_renderer          -> samaaja/page_renderers.py is gone; keeping this
#                             line would crash every page load.
#   website_route_rules    -> pointed at www/user-profile and www/campaign,
#                             both deleted. Vue serves those screens now.
#   has_website_permission -> the Events doctype has no web view, so this was
#                             never called.
#   profile_url_prefix     -> for Frappe's own /users/ profile pages, which we
#                             no longer expose.


doc_events = {
   "Events": {
        "on_update": [
            "samaaja.doc_events.events.update_subcategory",
            "samaaja.doc_events.events.update_profile_hook",
        ],
        "after_insert": [
			"samaaja.doc_events.action.after_insert",
            "samaaja.doc_events.events.update_profile_hook",
		],
        "on_trash": "samaaja.doc_events.events.update_profile_hook",
    },
    "Action": {
        "after_insert": "samaaja.doc_events.action.after_insert"
    },
        "Project Task": {
        "after_insert": "samaaja.doc_events.project_task.after_insert"
    },
    "User": {
        "after_insert": "samaaja.doc_events.user.after_insert",
        "on_trash": "samaaja.doc_events.user.on_trash"
    },
    "Organization":{
        "before_save":"samaaja.api.common.update_organization_id_case"
    },
    "User Metadata": {
        "validate": "samaaja.doc_events.user_metadata.on_save"
    },
    "Samaaja Settings": {
        "validate": "samaaja.doc_events.samaaja_settings.validate"
    },
    "Social Login Key": {
        "validate": "samaaja.doc_events.samaaja_settings.validate_social_login_key",
        "on_trash": "samaaja.doc_events.samaaja_settings.on_trash_social_login_key"
    },
    "Energy Point Log": {
        "before_insert": "samaaja.doc_events.energy_point_log.before_insert"
    },
    # Stops an admin creating a Web Page or Web Form at an address the Vue app
    # already owns - it would save fine and then never be reachable.
    "Web Page": {
        "validate": "samaaja.utils.route_check.validate_route_not_claimed"
    },
    "Web Form": {
        "validate": "samaaja.utils.route_check.validate_route_not_claimed"
    },
    "Event": {
        "validate": "samaaja.doc_events.event.generate_check_in_qr"
    },
}

fixtures = ["Client Script"]
on_session_creation = "samaaja.utils.cookie_patch.apply_patch"
