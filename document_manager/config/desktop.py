# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"module_name": "Document Manager",
			"color": "grey",
			"icon": "octicon octicon-file-directory",
			"type": "module",
			"label": _("Document Manager")
		},
		{
			"module_name": "Client",
			"color": "#f5ebff",
			"icon": "octicon octicon-briefcase",
			"label": _("Client"),
			"link": "List/Client",
			"_doctype": "Client",
			"type": "list"
		},
	]
