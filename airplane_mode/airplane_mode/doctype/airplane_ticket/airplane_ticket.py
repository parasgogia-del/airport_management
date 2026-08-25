# Copyright (c) 2026, paras and contributors
# For license information, please see license.txt

import frappe
import random
from frappe.model.document import Document


class AirplaneTicket(Document):


    def before_insert(self):

        self.assign_seat()
        self.set_gate_number()

        number = random.randint(10,99)
        letter = random.choice(["A","B","C","D","E"])

        self.seat = f"{number}{letter}"


    def assign_seat(self):

        number = random.randint(1, 99)
        letter = random.choice(["A", "B", "C", "D", "E"])

        self.seat = f"{number}{letter}"

    def set_gate_number(self):

        self.gate_number = frappe.db.get_value(
            "Airplane Flight",
            self.flight,
            "gate_number"
        )

    def validate(self):

        flight = frappe.get_doc(
            "Airplane Flight",
            self.flight
        )

        airplane = frappe.get_doc(
            "Airplane",
            flight.airplane
        )

        tickets = frappe.db.count(
            "Airplane Ticket",
            {
                "flight": self.flight
            }
        )

        if tickets >airplane.capacity:
            frappe.throw("Flight is Full")

        self.calculate_total_amount()
        self.remove_duplicate_addons()


    def calculate_total_amount(self):

        addon_total = 0

        for item in self.add_ons:
            addon_total += item.amount

        self.total_amount = self.flight_price + addon_total


    def remove_duplicate_addons(self):

        unique_items = []

        seen = set()

        for item in self.add_ons:

            if item.item not in seen:
                unique_items.append(item)
                seen.add(item.item)

        self.set("add_ons", unique_items)


    def before_submit(self):

        if self.status != "Boarded":

            frappe.throw(
                "Ticket can only be submitted after passenger is boarded"
            )
    pass
