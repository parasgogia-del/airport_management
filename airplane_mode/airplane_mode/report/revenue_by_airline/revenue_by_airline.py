# Copyright (c) 2026, ayush and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns = get_columns()
    data = get_data()
    chart = get_chart(data)
    summary = get_summary(data)

    return columns, data, None, chart, summary


def get_columns():
    return [
        {
            "label": "Airline",
            "fieldname": "airline",
            "fieldtype": "Link",
            "options": "Airline",
            "width": 250,
        },
        {
            "label": "Revenue",
            "fieldname": "revenue",
            "fieldtype": "Currency",
            "width": 150,
        },
    ]


def get_data():
    data = []

    airlines = frappe.get_all(
        "Airline",
        fields=["name"],
        order_by="name"
    )

    for airline in airlines:
        revenue = 0

        flights = frappe.get_all(
            "Airplane Flight",
            fields=["name", "airplane"]
        )

        for flight in flights:
            airplane_airline = frappe.db.get_value(
                "Airplane",
                flight.airplane,
                "airline"
            )

            if airplane_airline != airline.name:
                continue

            tickets = frappe.get_all(
                "Airplane Ticket",
                filters={
                    "flight": flight.name,
                    "docstatus": 1
                },
                fields=["total_amount"]
            )

            for ticket in tickets:
                revenue += ticket.total_amount or 0

        data.append({
            "airline": airline.name,
            "revenue": revenue
        })

    return data


def get_chart(data):
    return {
        "data": {
            "labels": [d["airline"] for d in data],
            "datasets": [
                {
                    "values": [d["revenue"] for d in data]
                }
            ]
        },
        "type": "line"
    }


def get_summary(data):
    total_revenue = sum(d["revenue"] for d in data)

    return [
        {
            "label": "Total Revenue",
            "value": total_revenue,
            "indicator": "Green",
            "datatype": "Currency",
        }
    ]
