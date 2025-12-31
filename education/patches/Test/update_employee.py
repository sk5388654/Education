import frappe

def execute():
    # Mapping of Employee ID (or name) -> last_name
    last_name_map = {
        "HR-EMP-00567": "Raja Hamza Shabbir",
        "HR-EMP-00568": "Shahnaz Bibi",
        "HR-EMP-00569": "Mehboob Alam",
        # add more as needed
    }

    for emp_id, last_name in last_name_map.items():
        frappe.db.set_value("Employee", emp_id, "last_name", last_name)
    
    frappe.db.commit()
