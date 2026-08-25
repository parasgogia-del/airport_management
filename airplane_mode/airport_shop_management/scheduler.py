import frappe

def send_rent_reminders():

    enabled = frappe.db.get_single_value(
        "Airport Shop Settings",
        "enable_rent_reminder"
    )

    if not enabled:
        return

    shops = frappe.get_all(
        "AirportShop",
        filters={
            "status": "Occupied"
        },
        fields=[
            "name",
            "tenant",
            "rent_amount"
        ]
    )

    for shop in shops:
        tenant = frappe.db.get_value(
            "Shop Tenant",
            shop.tenant,
            ["tenant_name", "email"],
            as_dict=True
        )

        if not tenant or not tenant.email:
            continue

        frappe.sendmail(
            recipients=[tenant.email],
            subject="Monthly Rent Reminder",
            message=f"""
                Dear {tenant.tenant_name},

                This is a reminder that your monthly rent of
                ₹ {shop.rent_amount} for shop {shop.name}
                is due.

                Thank you.
            """
        )
