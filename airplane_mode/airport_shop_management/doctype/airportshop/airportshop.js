// Copyright (c) 2026, paras and contributors
// For license information, please see license.txt

frappe.ui.form.on("AirportShop", {
	refresh(frm) {},

	setup(frm) {
        frm.set_query("shop_type", function () {
            return {
                filters: {
					enabled: 1
                }
            };
        });
    }
});
