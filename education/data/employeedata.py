import frappe
import json
import os
from frappe.utils import get_datetime

def import_employees():
    json_file_path = os.path.join(os.path.dirname(__file__), "employees.json")

    if not os.path.exists(json_file_path):
        frappe.throw(f"JSON file not found at {json_file_path}")

    with open(json_file_path) as f:
        employees = json.load(f)

    for emp in employees:
        try:
            employee_name = emp.get("name") or emp.get("employee") or emp.get("employee_name")

            company_name = emp.get("company")
            if company_name:
                if not frappe.db.exists("Company", company_name):
                    company_doc = frappe.get_doc({
                        "doctype": "Company",
                        "company_name": company_name,
                        "default_currency": "PKR"
                    })
                    company_doc.flags.ignore_mandatory = True
                    company_doc.insert(ignore_permissions=True)

            department_name = emp.get("department")
            if department_name and not frappe.db.exists("Department", department_name):
                dep_doc = frappe.get_doc({
                    "doctype": "Department",
                    "department_name": department_name,
                    "company": company_name or ""
                })
                dep_doc.flags.ignore_mandatory = True
                dep_doc.insert(ignore_permissions=True)

            designation_name = emp.get("designation")
            if designation_name and not frappe.db.exists("Designation", designation_name):
                des_doc = frappe.get_doc({
                    "doctype": "Designation",
                    "designation": designation_name,
                    "company": company_name or ""
                })
                des_doc.flags.ignore_mandatory = True
                des_doc.insert(ignore_permissions=True)

            branch_name = emp.get("branch")
            if branch_name and not frappe.db.exists("Branch", branch_name):
                br_doc = frappe.get_doc({
                    "doctype": "Branch",
                    "branch": branch_name
                })
                br_doc.flags.ignore_mandatory = True
                br_doc.insert(ignore_permissions=True)

            user_id = emp.get("user_id")
            if user_id and not frappe.db.exists("User", user_id):
                user_doc = frappe.get_doc({
                    "doctype": "User",
                    "email": user_id,
                    "first_name": emp.get("first_name") or (emp.get("employee_name") or "").split()[0],
                    "enabled": 1
                })
                user_doc.flags.ignore_mandatory = True
                user_doc.insert(ignore_permissions=True)

            if employee_name and frappe.db.exists("Employee", employee_name):
                doc = frappe.get_doc("Employee", employee_name)

                for k, v in emp.items():
                    if k not in ("name", "doctype") and not isinstance(v, list):
                        setattr(doc, k, v)

                for table_field in doc.meta.get_table_fields():
                    if table_field in emp and isinstance(emp[table_field], list):
                        doc.set(table_field, [])
                        for child_row in emp[table_field]:
                            doc.append(table_field, child_row)

                doc.flags.ignore_mandatory = True
                doc.flags.ignore_validate = True
                doc.flags.ignore_validate_update_after_submit = True

                doc.save(ignore_permissions=True)

                print(f"Updated employee: {emp.get('employee_name')}")

            else:
                doc = frappe.get_doc({"doctype": "Employee", **emp})
                doc.flags.ignore_mandatory = True
                doc.flags.ignore_validate = True
                doc.flags.ignore_validate_update_after_submit = True
                doc.insert(ignore_permissions=True)
                print(f"Inserted employee: {emp.get('employee_name')}")

            old_creation = emp.get("creation")
            old_modified = emp.get("modified")

            if old_creation:
                doc.db_set("creation", get_datetime(old_creation), update_modified=False)
            if old_modified:
                doc.db_set("modified", get_datetime(old_modified), update_modified=False)

            frappe.db.commit()

        except Exception as e:
            print(f"Error inserting/updating {emp.get('employee_name')}: {e}")
