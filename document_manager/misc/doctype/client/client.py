# -*- coding: utf-8 -*-
# Copyright (c) 2017, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import json

import frappe
from frappe.model.document import Document


class Client(Document):
    # When a new client is created,  we need to create a new folder in the manager
    # Then we create a new user_role and admin_role
    # Admin can then assign new roles to all users

    def validate(self):
        pass


    def after_insert(self):
        # we the add the file manager for the client and do some
        parent = ""
        folders = []
        root = "Home"
        client_name = self.client_name
        client_user_roles = []
        client_admin_role = "{0} - Admin".format(client_name)
        client_user_role = "{0} - User".format(client_name)

        if self.create_new_structure == 1:
            # Client Structure Predefined
            if self.use_default == 1:
                client_structure = get_structure(client=client_name, is_default=1)
            else :
                if self.folder_structure:
                    client_structure = get_structure(structure=self.folder_structure,client=client_name)

            for (key, client) in client_structure.items():
                if parent is "":
                    parent = _p = "{0}".format(root)
                    folders.append({"parent": parent, "folder_name": key})
                if isinstance(client, dict):
                    for (k, v) in client.items():
                        role = "{0} - {1} - User".format(client_name, k)
                        parent = "{0}/{1}".format(_p, key)
                        folders.append({"parent": parent, "folder_name": k, "role": role})
                        if role not in client_user_roles:
                            client_user_roles.append(role)
                        if isinstance(v, list):
                            for i in v:
                                folders.append({"parent": "{0}/{1}".format(parent, k), "folder_name": i, "role": role})

            if folders:
                create_new_role(client_user_role)
                create_new_role(client_admin_role)
                for role in client_user_roles:
                    create_new_role(role)

            for folder in folders:
                # create user and pass admin
                if not folder.get('parent') == root:
                    c = folder.get('role')
                else:
                    c = client_user_role

                create_new_folder(folder.get('folder_name'), folder.get('parent'), c, client_admin_role)




def get_structure(structure = None, client = None, is_default = False):
    default = 0
    if is_default == 1:
        default  = 1
    def get_children(structure, parent):
        if not default :
            if parent != "root":
                ls = frappe.db.sql("select fsi.child from `tabFolder Structure` fs inner join `tabFolder Structure Item` fsi "
                                   "where (fsi.parent = fs.name) and (fs.name = '{structure}')  and fsi.parent_folder="
                                   "'{parent}' and fs.is_default=0".format(structure=structure, parent=parent), as_list=1)
            else:
                ls = frappe.db.sql("select fsi.child from `tabFolder Structure` fs inner join `tabFolder Structure Item` fsi "
                                   "where (fsi.parent = fs.name) and (fs.name = '{structure}')  and fsi.is_root=1 and fs.is_default=0"
                                   .format(structure=structure), as_list=1)
        else:
            if parent != "root":
                ls = frappe.db.sql(
                    "select fsi.child from `tabFolder Structure` fs inner join `tabFolder Structure Item` fsi "
                    "where (fsi.parent = fs.name) and fsi.parent_folder='{parent}' and fs.is_default=1"
                    .format(parent=parent), as_list=1)

            else:
                ls = frappe.db.sql(
                    "select fsi.child from `tabFolder Structure` fs inner join `tabFolder Structure Item` fsi "
                    "where (fsi.parent = fs.name) and fsi.is_root=1 and fs.is_default=1", as_list=1)

        return [x[0] for x in ls]

    ls = {}
    for v in get_children(structure, "root"):
        _ = get_children(structure, v)
        if _ == []:
            x = v
        else:
            x = _
        ls.update({ v: x })

    print  { client : ls}
    return { client : ls}


def create_new_folder(file_name, folder, user, admin):
    file = frappe.new_doc("File")
    file.file_name = file_name
    file.is_folder = 1
    file.folder = folder
    file.file_user = user
    file.file_admin = admin
    file.insert()


def create_new_role(role):
    l = frappe.get_doc({
        "role_name": role,
        "doctype": "Role",
        "desk_access": 0
    })
    l.insert()

@frappe.whitelist()
def get_permission_query_conditions_for_file(user):
    roles = ','.join([str("\"" + i + "\"") for i in frappe.get_roles(user)])
    roled = "select tabFile.name from tabFile where (tabFile.file_user in ({roles}) or tabFile.file_admin in ({roles}))"
    if "System Manager" in frappe.get_roles(user):
        return None
    elif "File User" in frappe.get_roles(user):
        return """(tabFile.owner = '{user}') or ((tabFile.is_folder = 0) and tabFile.folder in ({roled})) or
        (tabFile.name in ({roled}))""".format(user=frappe.db.escape(user), roled=roled.format(roles=roles))
