# Copyright (c) 2023, Bernhard Hein and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
from datetime import datetime


class Monat(Document):
    def before_save(self):
        pass #calculate_startbetrag(self)

@frappe.whitelist()
def get_monat_count():
    return frappe.db.count('Monat')


@frappe.whitelist()
def custom_query_function(doctype, txt, searchfield, start, page_len, filters):
    current_monat_name = filters.get('current_monat')
    current_monat = frappe.get_doc('Monat', current_monat_name)

    return frappe.db.sql("""
        SELECT `name`, `monat`
        FROM `tabMonat`
        WHERE
            `monat_davor` IS NULL
            AND `creation` < %s
            AND (`name` LIKE %s OR `monat` LIKE %s)
        ORDER BY `creation` DESC
        LIMIT %s, %s
    """, (current_monat.creation, f'%{txt}%', f'%{txt}%', start, page_len), as_list=True)

def autoname(self):
    # Dictionary to map English month names to German
    months_german = {
        "January": "Januar", "February": "Februar", "March": "März",
        "April": "April", "May": "Mai", "June": "Juni",
        "July": "Juli", "August": "August", "September": "September",
        "October": "Oktober", "November": "November", "December": "Dezember"
    }

    # Parse the date string
    date = datetime.strptime(self.datum, "%Y-%m-%d")

    # Format the date as "M-Month-Year" using German month names
    formatted_date = f"M-{months_german[date.strftime('%B')]}-{date.year}"
    return formatted_date



@frappe.whitelist()
def get_endbetrag_items(parent_name):
    if not frappe.db.exists('Monat', parent_name):
        return []
    frappe.get_doc()
    endbetrag_items = frappe.get_all('Endbetrag Item',
                                   fields=['heigh', 'kategorie'],
                                   filters={'parent': parent_name, 'parentfield': 'tbl_endbetrag'})
    return endbetrag_items


