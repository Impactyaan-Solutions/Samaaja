frappe.provide("samaaja.setup");

frappe.setup.on("before_load", function () {
	if (frappe.boot.setup_wizard_completed_apps?.includes("samaaja")) return;
	samaaja.setup.slides_settings.map(frappe.setup.add_slide);
});

samaaja.setup.slides_settings = [
	{
		name: "samaaja_branding",
		title: __("Brand your Samaaja"),
		help: __(
			"Everything here is optional and can be changed later in Samaaja Settings."
		),
		fields: [
			{
				fieldname: "app_logo",
				label: __("Logo"),
				fieldtype: "Attach",
			},
			{
				fieldname: "app_name",
				label: __("App Name"),
				fieldtype: "Data",
				default: "Samaaja",
				reqd: 1,
			},
			{
				fieldname: "tagline",
				label: __("Tagline"),
				fieldtype: "Data",
				description: __("Shown on the landing page, under the app name."),
			},
			{
				fieldname: "primary_color",
				label: __("Primary Color"),
				fieldtype: "Color",
			},
			{
				fieldname: "accent_color",
				label: __("Accent Color"),
				fieldtype: "Color",
			},
		],
	},
];
