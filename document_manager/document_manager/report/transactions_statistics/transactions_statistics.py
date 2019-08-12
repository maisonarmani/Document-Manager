# Copyright (c) 2013, masonarmani and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns = [
		{
			"fieldname": "Document",
			"label": "Document",
			"fieldtype": "Data",
			"width": 110
		},{
			"fieldname": "Transaction Count",
			"label": "Transaction Count",
			"fieldtype": "Float",
			"width": 200
		}
	]

	data = []
	conditions = ""

	if filters.get('from_date') and filters.get('to_date'):
		conditions += "posting_date between '{from_date}' and '{to_date}'"

	query = "select count(name) from `{0}` where {conditions}"

	for table in ["tabPayment Entry", "tabSales Invoice","tabPurchase Receipt","tabJournal Entry"]:
		res = frappe.db.sql(query.format(table, conditions=conditions.format(**filters)))
		data.append((table.replace("tab", ""), res[0][0], ""))

	return columns, data
