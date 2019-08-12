// Copyright (c) 2016, masonarmani and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Regional Performance"] = {
	"filters": [{
			"fieldname": "fiscal_year",
			"label": __("Fiscal Year"),
			"fieldtype": "Link",
			"options":"Fiscal Year",
			"reqd":1
		},
		{
			"fieldname": "month",
			"label": __("Month"),
			"fieldtype": "Select",
			"options": "January\nFebruary\nMarch\nApril\nMay\nJune\nJuly\nAugust\nSeptember\nOctober\nNovember\nDecember",
			"reqd":1
		},
		{
			"fieldname": "region",
			"label": __("Region"),
			"fieldtype": "Link",
			"options":"Territory",
			"reqd":1
		}

	]
};
