frappe.provide("samaaja.setup");

frappe.setup.on("before_load", function () {
	if (frappe.boot.setup_wizard_completed_apps?.includes("samaaja")) return;
	samaaja.setup.slides_settings.map(frappe.setup.add_slide);
});

samaaja.setup.slides_settings = [
	{
		name: "samaaja_authentication",
		title: __("Samaaja sign-in"),
		help: __(
			"Phone number + password is on by default. Everything below is optional and can be changed later in Samaaja Settings and Social Login Key."
		),
		fields: [
			{
				fieldname: "enable_otp_login",
				label: __("Use OTP instead of password"),
				fieldtype: "Check",
			},
			{
				fieldname: "google_section",
				label: __("Google"),
				fieldtype: "Section Break",
			},
			{
				fieldname: "enable_google",
				label: __("Enable Google sign-in"),
				fieldtype: "Check",
			},
			{
				fieldname: "google_client_id",
				label: __("Client ID"),
				fieldtype: "Data",
				depends_on: "eval:doc.enable_google",
				mandatory_depends_on: "eval:doc.enable_google",
			},
			{
				fieldname: "google_client_secret",
				label: __("Client Secret"),
				fieldtype: "Password",
				depends_on: "eval:doc.enable_google",
				mandatory_depends_on: "eval:doc.enable_google",
			},
			{
				fieldname: "facebook_section",
				label: __("Facebook"),
				fieldtype: "Section Break",
			},
			{
				fieldname: "enable_facebook",
				label: __("Enable Facebook sign-in"),
				fieldtype: "Check",
			},
			{
				fieldname: "facebook_client_id",
				label: __("Client ID"),
				fieldtype: "Data",
				depends_on: "eval:doc.enable_facebook",
				mandatory_depends_on: "eval:doc.enable_facebook",
			},
			{
				fieldname: "facebook_client_secret",
				label: __("Client Secret"),
				fieldtype: "Password",
				depends_on: "eval:doc.enable_facebook",
				mandatory_depends_on: "eval:doc.enable_facebook",
			},
		],
	},
];
