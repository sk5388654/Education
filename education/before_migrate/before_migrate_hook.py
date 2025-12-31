import frappe

def backup_critical_data():
    data = frappe.get_all("Delivery Note Item")
    with open("/tmp/items_table.json", "w") as f:
        import json
        json.dump(data, f)
    frappe.logger().info("Backed up My Doctype before migration")
