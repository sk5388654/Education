# import frappe
# import json
# import os
# from frappe.utils import get_datetime

# def import_users():
#     json_file_path = os.path.join(os.path.dirname(__file__), "users.json")

#     if not os.path.exists(json_file_path):
#         frappe.throw(f"JSON file not found at {json_file_path}")

#     with open(json_file_path) as f:
#         users = json.load(f)

#     for usr in users:
#         try:
#             user_email = usr.get("name") or usr.get("email")
#             if not user_email:
#                 print("Skipping record (no email/name)")
#                 continue

#             # Remove employee/user_id references from JSON
#             usr.pop("employee", None)
#             usr.pop("user_id", None)

#             # Ensure Roles exist
#             for role in usr.get("roles", []):
#                 role_name = role.get("role")
#                 if role_name and not frappe.db.exists("Role", role_name):
#                     frappe.get_doc({
#                         "doctype": "Role",
#                         "role_name": role_name
#                     }).insert(ignore_permissions=True)

#             # Ensure User Groups exist
#             for ug in usr.get("user_groups", []):
#                 ug_name = ug.get("user_group")
#                 if ug_name and not frappe.db.exists("User Group", ug_name):
#                     frappe.get_doc({
#                         "doctype": "User Group",
#                         "user_group_name": ug_name
#                     }).insert(ignore_permissions=True)

#             # Disable email sending during migration
#             frappe.local.flags.mute_emails = True

#             if frappe.db.exists("User", user_email):
#                 doc = frappe.get_doc("User", user_email)

#                 # Skip system users
#                 if doc.name in ("Guest", "Administrator"):
#                     print(f"Skipping system user: {user_email}")
#                     continue

#                 # Skip if linked Employee does not exist
#                 if getattr(doc, "employee", None) and not frappe.db.exists("Employee", doc.employee):
#                     print(f"Skipping user {user_email}: linked Employee {doc.employee} not found")
#                     continue

#                 # Update simple fields
#                 for k, v in usr.items():
#                     if k not in ["roles", "user_groups", "doctype"] and not isinstance(v, list):
#                         setattr(doc, k, v)

#                 doc.username = usr.get("username") or usr.get("email")

#                 # Clear Employee link to avoid validation
#                 if hasattr(doc, "employee"):
#                     doc.employee = None

#                 # Update roles
#                 doc.set("roles", [])
#                 for r in usr.get("roles", []):
#                     doc.append("roles", r)

#                 # Update user groups
#                 if "user_groups" in doc.meta.get_table_fields():
#                     doc.set("user_groups", [])
#                     for ug in usr.get("user_groups", []):
#                         doc.append("user_groups", ug)

#                 # Save first
#                 doc.flags.ignore_version = True
#                 doc.flags.ignore_mandatory = True
#                 doc.flags.ignore_validate = True
#                 doc.flags.ignore_validate_update_after_submit = True
#                 doc.save(ignore_permissions=True)

#                 # Set creation and modified timestamps
#                 if usr.get("creation"):
#                     doc.db_set("creation", get_datetime(usr.get("creation")), update_modified=False)
#                 if usr.get("modified"):
#                     doc.db_set("modified", get_datetime(usr.get("modified")), update_modified=False)

#                 print(f"Updated user: {user_email}")

#             else:
#                 # New user
#                 doc = frappe.get_doc({"doctype": "User", **usr})
#                 doc.username = usr.get("username") or usr.get("email")

#                 # Clear Employee link
#                 if hasattr(doc, "employee"):
#                     doc.employee = None

#                 doc.flags.ignore_mandatory = True
#                 doc.flags.ignore_validate = True
#                 doc.insert(ignore_permissions=True)

#                 if usr.get("creation"):
#                     doc.db_set("creation", get_datetime(usr.get("creation")), update_modified=False)
#                 if usr.get("modified"):
#                     doc.db_set("modified", get_datetime(usr.get("modified")), update_modified=False)

#                 print(f"Inserted user: {user_email}")

#             frappe.db.commit()

#         except Exception as e:
#             print(f"Error inserting/updating user {usr.get('email')}: {e}")

