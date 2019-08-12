// Copyright (c) 2016, masonarmani and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Transactions Statistics"] = {
	"filters": [{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"reqd":1,
			"default":frappe.datetime.get_today()
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd":1,
			"default":frappe.datetime.add_days(frappe.datetime.get_today(),7)
		}
	]
};
