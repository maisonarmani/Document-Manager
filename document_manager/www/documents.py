# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import db

no_sitemap = 1
no_cache = 1


def get_context(context):
    #file_user = frappe.db.get_value("File User",
                                      #{"parent": frappe.form_dict.project, "user": frappe.session.user}, "user")
    #if not file_user or frappe.session.user == 'Guest':
        #raise frappe.PermissionError
    context.no_cache = 1
    context.show_sidebar = True

    files = get_base_files()
    context.docs = files

@frappe.whitelist(False)
def _get_children(parent = "Home"):
    user = frappe.session.user
    if frappe.form_dict.name is not None:
        parent = frappe.form_dict.name
    sql = "select file_name,file_url,old_parent,is_folder from `tabFile` where ({}) and (old_parent = '{parent}')"\
        .format(get_permission_query_conditions_for_file(user), parent=parent)
    data = db.sql(sql, as_dict=1)
    return data


def get_permission_query_conditions_for_file(user):
    roles = ','.join([str("\"" + i + "\"") for i in frappe.get_roles(user)])
    roled = "select tabFile.name from tabFile where (tabFile.file_user in ({roles}) or tabFile.file_admin in ({roles}))"
    if "System Manager" in frappe.get_roles(user):
        return "1=1"
    elif "File User" in frappe.get_roles(user):
        return """(tabFile.owner = '{user}') or ((tabFile.is_folder = 0) and tabFile.folder in ({roled})) or
        (tabFile.name in ({roled}))""".format(user=frappe.db.escape(user), roled=roled.format(roles=roles))


def get_base_files():
    return _get_children()
