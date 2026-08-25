# Copyright (c) 2026, paras and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ShopRentalContract(Document):

    def validate(self):
        self.validate_contract_dates()
        self.validate_active_contract()

    def on_submit(self):
        self.update_shop_status("Occupied")

    def on_cancel(self):
        self.update_shop_status("Available")


    def update_shop_status(self, status):

        frappe.db.set_value(
            "AirportShop",
            self.airport_shop,
            "status",
            status
        )
        frappe.db.commit()

    def validate_contract_dates(self):

        if self.contract_start_date and self.contract_end_date:

            if self.contract_end_date<=self.contract_start_date:

                frappe.throw(
					"Contract End Date must be after Contract Start Date."
				)


    def validate_active_contract(self):

        if self.status!="Active":
            return

        existing_contract = frappe.get_all(
            "Shop Rental Contract",
            filters={
                "airport_shop": self.airport_shop,
                "status": "Active",
                "name": ["!=", self.name]
            },
            fields=["name", "tenant"]
		)


        if existing_contract:
            frappe.throw(
				f"Shop {self.airport_shop} already has an active contract."
			)
