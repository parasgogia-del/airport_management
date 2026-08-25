// Copyright (c) 2026, paras and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Flight", {
	refresh(frm) {
		set_crew_filter(frm);
	},

	airplane(frm) {
		// Remove old crew members
		frm.clear_table("crew_members");
		frm.refresh_field("crew_members");

		// Apply new filter
		set_crew_filter(frm);
	},
});

function set_crew_filter(frm) {
	frm.fields_dict.crew_members.grid.get_field("crew_member").get_query = function () {
		return {
			filters: {
				airline: frm.doc.airline,
			},
		};
	};
}

frappe.ui.form.on("Flight Crew Assignment", {
	crew_member(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		let duplicate = frm.doc.crew_members.filter((d) => d.crew_member === row.crew_member);
		if (duplicate.length > 1) {
			frappe.msgprint("Crew Member is already added.");
			row.crew_member = "";
			frm.refresh_field("crew_members");
		}
	},
});
