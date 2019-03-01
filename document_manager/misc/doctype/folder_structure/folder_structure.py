# -*- coding: utf-8 -*-
# Copyright (c) 2017, masonarmani and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class FolderStructure(Document):
    def validate(self):
        if self.is_default == 1:
            ls = frappe.db.sql("select name from `tabFolder Structure` where is_default = 1", as_dict=1)

            if len(ls) > 0:
                if ls[0].get('name') != self.name:
                    frappe.throw("Sorry. Only one default folder structure can exist.")


@frappe.whitelist()
def get_children():
    args = frappe.local.form_dict
    if args.get("type"):
        doctype, type = args['doctype'], args['type']
        fieldname = frappe.db.escape(doctype.lower().replace(' ', '_'))
        doctype = frappe.db.escape(doctype)

        # root
        if args['parent'] in ("Folder Structure"):
            fields = ", folder_structure_type,parent_tree "
            acc = frappe.db.sql(""" select
				name as value, is_group as expandable {fields}
				from `tab{doctype}`
				where ifnull(`parent_{fieldname}`,'') = ''
				and `folder_structure_type` = %s	and docstatus < 2
				order by name""".format(fields=fields, fieldname=fieldname, doctype=doctype),
                                type, as_dict=1)

        return acc
    return {}
