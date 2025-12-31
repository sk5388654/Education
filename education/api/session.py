import frappe


@frappe.whilelist()
def get_session_details():
    user = frappe.get_doc("User", frappe.session.user)
    user_details = {
        "full_name": user.full_name,
        "email": user.email,
        "roles": user.get_roles(),
        "language": user.language,
    }
    return user_details