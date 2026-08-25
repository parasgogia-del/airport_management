# Copyright (c) 2026, paras and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator


class AirportShop(WebsiteGenerator):

    def validate(self):
        self.set_default_rent()

    def after_insert(self):
        self.update_statistics()

    def on_update(self):
        self.update_statistics()

    def on_trash(self):
        self.update_airport(self.airport)

    def set_default_rent(self):
        if not self.rent_amount:
            rent = frappe.db.get_single_value(
                "Airport Shop Settings",
                "default_rent_amount"
            )
            if rent:
                self.rent_amount = rent

    def update_statistics(self):
        # Update current airport
        self.update_airport(self.airport)

        # If airport changed, update old airport too
        if not self.is_new():
            old_doc = self.get_doc_before_save()

            if old_doc and old_doc.airport != self.airport:
                self.update_airport(old_doc.airport)

    def update_airport(self, airport):

        if not airport:
            return

        total = frappe.db.count(
            "AirportShop",
            {"airport": airport}
        )

        occupied = frappe.db.count(
            "AirportShop",
            {
                "airport": airport,
                "status": "Occupied"
            }
        )

        available = frappe.db.count(
            "AirportShop",
            {
                "airport": airport,
                "status": "Available"
            }
        )

        frappe.db.set_value(
            "Airport",
            airport,
            {
                "total_shops": total,
                "occupied_shops": occupied,
                "available_shops": available
            }
        )
