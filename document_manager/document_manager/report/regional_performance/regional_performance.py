# Copyright (c) 2019, masonarmani and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import math

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
			" COUNT(i.item_code) cnt,dn.territory," \
			" SUM(dni.qty) qty, SUM(dni.rate) rate ,SUM(dni.amount) amount" \
			" FROM `tabItem` i INNER JOIN `tabDelivery Note Item` dni " \
			" ON(i.item_code = dni.item_code) INNER JOIN `tabDelivery Note` dn ON(dni.parent = dn.name) INNER JOIN" \
			" `tabCustomer` customer ON(dn.customer = customer.name) " \
			" WHERE dn.docstatus != 2 AND {0} GROUP BY i.item_code".format(conditions)


	result = frappe.db.sql(query, as_dict=1)

	for dt in result :
		target = get_target(dt.get("item_code"), dt.get("territory"),filters.get('month'))
		data.append({
			"item_code": dt.get("item_code"),
			"qty":dt.get("qty"),
			"average_rate":dt.get("rate") / dt.get("cnt"),
			"target_sales":target.get('target_qty'),
			"total_amount_budget_sales": target.get('target_amount'),
			"total_amount":dt.get("amount"),
			"unit_price":dt.get("price_list_rate"),
			"variance_amount":target.get('target_amount') - dt.get("amount"),
			"variance_qty": target.get('target_qty') - dt.get("qty"),
			"variance_percentage": 100 * math.fabs(target.get('target_qty') - dt.get("qty")) / ((target.get('target_qty') - dt.get("qty")) / 2)
		})

	return data


def wordtonumber(month):
	d = ["January","February","March","April","May","June","July","August","September","October","November","December"]
	return d.index(month) + 1


def get_target(item, territory, month):
	# get item target for selected territory
	# and then get the distribution information

	query = "SELECT SUM(t.target_qty) target_qty, SUM(t.target_amount) target_amount, " \
			" t.fiscal_year, dp.month, t .distribution_id , dp.percentage_allocation FROM " \
			" `tabTerritory` p INNER JOIN `tabItem Target Detail` t ON (p.name = t.parent) " \
			" INNER JOIN `tabMonthly Distribution` d ON(p.distribution_id = d.name)  INNER JOIN" \
			" `tabMonthly Distribution Percentage` dp ON(dp.parent = d.name) " \
			" WHERE t.item = '{0}' AND (p.name='{1}' " \
			"OR parent_territory = '{1}')  AND dp.month = '{2}'  GROUP BY t.item" .format(item,territory, month)

	result = frappe.db.sql(query, as_dict=1)

	target = dict(target_qty=0,target_amount=0)
	for value in result:
		target.update({
			"target_qty": (value.get('target_qty') / 100) * value.get('percentage_allocation') or 0,
			"target_amount": (value.get('target_amount') / 100) * value.get('percentage_allocation') or 0,
		})
	return target

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
			"fieldtype": "Float",
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
			"fieldname": "variance_qty",
			"label": "Variance (Qty)",
			"fieldtype": "Float",
			"width": 120
		},{
			"fieldname": "variance_percentage",
			"label": "Variance (Percentage)",
			"fieldtype": "Float",
			"width": 120
		},
	]

