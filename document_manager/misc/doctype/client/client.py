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
    def on_save(self):
        pass

    def validate(self):
        pass

    def autoname(self):
        pass

    def before_save(self):
        frappe.errprint(self.name)

    def after_save(self):
        frappe.errprint(self.name)

    def before_insert(self):
        frappe.errprint("before insert")

    def after_insert(self):
        # we the add the file manager for the client and do some
        parent = ""
        folders = []
        root = "Home"
        client_name = self.client_name
        client_user_roles = []
        client_admin_role = "{0} - Admin".format(client_name)
        client_user_role = "{0} - User".format(client_name)

        # Client Structure Predefined
        client_structure = {
            client_name: {
                "Awards Papers": ["MVC", "Polo"],
                "Certificates": "Certificates",
                "Demo Files": "Demo Files",
                "Credentials": "Credentials",
                "Licenses": "Licenses",
            }
        }

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

        for indx, folder in enumerate(folders):
            # create user and pass admin
            if not folder.get('parent') == root:
                c = folder.get('role')
            else:
                c = client_user_role

            create_new_folder(folder.get('folder_name'), folder.get('parent'), c, client_admin_role)

    def before_submit(self):
        frappe.errprint("before submit")

    def before_cancel(self):
        pass

    def before_update_after_submit(self):
        pass

    def on_update(self):
        pass

    def on_submit(self):
        pass

    def on_cancel(self):
        pass

    def on_update_after_submit(self):
        pass

    def on_change(self):
        pass

    def on_trash(self):
        pass

    def after_delete(self):
        pass


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
