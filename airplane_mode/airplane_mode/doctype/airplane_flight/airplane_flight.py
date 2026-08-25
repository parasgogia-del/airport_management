# Copyright (c) 2026, paras and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator


class AirplaneFlight(WebsiteGenerator):


    def on_update(self):

        old_doc = self.get_doc_before_save()

        if old_doc and old_doc.gate_number != self.gate_number:

            frappe.enqueue(
                "airplane_mode.background_jobs.update_gate_numbers",
                flight=self.name,
                gate_number=self.gate_number
            )

    def on_submit(self):
        self.db_set("status", "Completed")
        pass


    def validate(self):
        self.validate_crew_roles()

    def validate_crew_roles(self):

        pilot_count = 0
        copilot_count = 0

        for row in self.crew_members:

            crew = frappe.get_doc("Flight Crew Member", row.crew_member)

            if crew.role == "Pilot":
                pilot_count += 1

            elif crew.role == "Co-Pilot":
                copilot_count += 1

        if pilot_count > 1:
            frappe.throw("Only one Pilot is allowed in a flight.")

        if copilot_count > 1:
            frappe.throw("Only one Co-Pilot is allowed in a flight.")
