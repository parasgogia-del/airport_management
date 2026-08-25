import frappe


def get_context(context):

    context.doc = frappe.get_doc(
        "Airplane Flight",
        frappe.form_dict.route
    )

    return context
