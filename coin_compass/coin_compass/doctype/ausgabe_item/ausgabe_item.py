# Copyright (c) 2024, Bernhard Hein and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe
from frappe import _

class AusgabeItem(Document):

    def on_update(self):
        # Code to execute when an Ausgabe Item is updated
        total_expenses = self.calculate_total_expenses_for_budget_item(self.budget)
        self.update_budget_item(self.budget, total_expenses)
        self.save_monat_document()

    def calculate_total_expenses_for_budget_item(self, budget_item_name):
        ausgaben = frappe.get_all('Ausgabe Item', filters={'budget': budget_item_name}, fields=['betrag'])
        total = sum(item.betrag for item in ausgaben)
        return total
    def update_budget_item(self, budget_item_name, total_expenses):
        budget_item = frappe.get_doc('Budget Item', budget_item_name)
        budget_item.ausgegeben = total_expenses
        budget_item.save()
        return 0
    def save_monat_document(ausgabe_item):
        monat = frappe.get_doc('Monat', ausgabe_item.parent_name)
        monat.save()
        

@frappe.whitelist()
def get_ausgabe_items(parent_name):
    if not frappe.db.exists('Monat', parent_name):
        return []
    ausgabe_items = frappe.get_all('Ausgabe Item',
                                   fields=['name', 'betrag','datum','kategorie','budget'],
                                   filters={'parent': parent_name, 'parentfield': 'tbl_ausgabe'})
    return ausgabe_items