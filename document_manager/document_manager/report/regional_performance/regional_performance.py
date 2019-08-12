# Copyright (c) 2019, masonarmani and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	return get_column(filters), get_data(filters)



def get_data(filters):
	data = []
	conditions = ""

	if filters.get('month') and filters.get('fiscal_year'):
		start_date = "%s-%s-01" % (filters.get('fiscal_year'), wordtonumber(filters.get('month')))
		end_date = "%s-%s-31" % (filters.get('fiscal_year'), wordtonumber(filters.get('month')))

		frappe.errprint(end_date)
		conditions += "dn.posting_date between DATE('%s') and DATE('%s')" % (start_date, end_date)

	if filters.get('region') :
		conditions += " AND customer.territory = '%s'" % filters.get('region')

	query = " SELECT DISTINCT i.item_code item_code, dni.price_list_rate price_list_rate,  " \
			" COUNT(i.item_code) cnt," \
			" SUM(dni.qty) qty, SUM(dni.rate) rate ,SUM(dni.amount) amount" \
			" FROM `tabItem` i INNER JOIN `tabDelivery Note Item` dni " \
			" ON(i.item_code = dni.item_code) INNER JOIN `tabDelivery Note` dn ON(dni.parent = dn.name) INNER JOIN" \
			" `tabCustomer` customer ON(dn.customer = customer.name) " \
			" WHERE dn.docstatus != 2 AND {0} GROUP BY i.item_code".format(conditions)

	frappe.errprint(query)

	result = frappe.db.sql(query, as_dict=1)

	for dt in result :
		data.append({
			"item_code": dt.get("item_code"),
			"qty":dt.get("qty"),
			"average_rate":dt.get("rate") / dt.get("cnt"),
			"target_sales":0,
			"total_amount_budget_sales": 0,
			"total_amount":dt.get("amount"),
			"unit_price":dt.get("price_list_rate"),
			"variance_amount":0,
			"variance_percentage":0,
			"variance_qty":0,
		})

	return data


def wordtonumber(month):
	d = ["January","February","March","April","May","June","July","August","September","October","November","December"]
	return d.index(month) + 1



def get_column(filters):
	return [{
			"fieldname": "item_code",
			"label": "Item Code",
			"fieldtype": "Link",
			"options":"Item",
			"width": 100
		},{
			"fieldname": "target_sales",
			"label": "Target Sales in %s " % filters.get("month"),
			"fieldtype": "Float",
			"width": 130
		},{
			"fieldname": "unit_price",
			"label": "Unit Price",
			"fieldtype": "Currency",
			"width": 120
		},{
			"fieldname": "total_amount_budget_sales",
			"label": "Total Sales in % s " % filters.get("month"),
			"fieldtype": "Currency",
			"width": 120
		},{
			"fieldname": "qty",
			"label": "Actual Sales in % s " % filters.get("month"),
			"fieldtype": "Currency",
			"width": 200
		},{
			"fieldname": "average_rate",
			"label": "Average Price Per Unit",
			"fieldtype": "Float",
			"width": 120
		},{
			"fieldname": "total_amount",
			"label": "Total Amount of Actual Sales",
			"fieldtype": "Currency",
			"width": 140
		},{
			"fieldname": "variance_amount",
			"label": "Variance (Amount)",
			"fieldtype": "Currency",
			"width": 120
		},{
			"fieldname": "variance_percentage",
			"label": "Variance (Percentage)",
			"fieldtype": "Float",
			"width": 120
		},{
			"fieldname": "variance_qty",
			"label": "Variance (Qty)",
			"fieldtype": "Float",
			"width": 120
		}
	]

