# Copyright (c) 2023, Bernhard Hein and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe
from frappe import _


class BudgetItem(Document):
	pass

@frappe.whitelist()
def get_budget_items(parent_name):
    if not frappe.db.exists('Monat', parent_name):
        return []

    budget_items = frappe.get_all('Budget Item',
                                  fields=['name', 'budget_name', 'betrag', 'von_budget'],
                                  filters={'parent': parent_name, 'parentfield': 'tbl_budget'})
    return budget_items