import frappe

def get_context(context):

    context.shops = frappe.get_all(
        "AirportShop",
        filters={
            "is_published": 1
        },
        fields=[
            "name",
            "shop_name",
            "shop_number",
            "airport",
            "rent_amount",
            "status",
            "route"
        ]
    )

    return context
