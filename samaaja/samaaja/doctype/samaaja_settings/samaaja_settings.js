// Copyright (c) 2023, Impactyaan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Samaaja Settings', {
	go_to_gender: function (frm) {
		frappe.set_route('List', 'Gender');
	},
	go_to_action_type: function (frm) {
		frappe.set_route('List', 'Action Type');
	},
	go_to_action_category: function (frm) {
		frappe.set_route('List', 'Action Category');
	},
	go_to_user_category: function (frm) {
		frappe.set_route('List', 'User Category');
	},
	go_to_badges: function (frm) {
		frappe.set_route('List', 'Badge');
	},
	go_to_energy_point_rule: function (frm) {
		frappe.set_route('List', 'Energy Point Rule');
	}
});
