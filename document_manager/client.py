# -*- coding: utf-8 -*-
# Copyright (c) 2017, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import share,_


def update_customer_folder_structure(customer):
    customer_email = customer.get('email')
    if customer_email is None:
        frappe.throw("Please provide customer user for new user")

    root = create_client_root_folder()

    folders, client_name = [], customer.name
    client_structure = get_structure(structure="Primary", client=client_name)
    folders.append({"parent":root, "folder_name": client_name})
    for (key, client) in client_structure.items():
        if isinstance(client, dict):
            for (k, v) in client.items():
                parent = "{0}/{1}".format(root, key)
                folders.append({"parent": parent, "folder_name": k})

                if isinstance(v, list):
                    for i in v:
                        folders.append({"parent": "{0}/{1}".format(parent, k), "folder_name": i})


    frappe.errprint("folders %s" % folders)
    for folder in folders:
        create_new_folder(folder.get('folder_name'), folder.get('parent'), customer_email)


def get_structure(structure=None, client=None):
    def get_children(structure, parent):
        # check if there's a default set
        check = frappe.db.sql(
            "select fsi.child from `tabFolder Structure` fs inner join `tabFolder Structure Item` fsi limit 1", as_list=1)

        if check == []:
            frappe.throw("Sorry, No folder structure found")

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
        ls.update({v: x})

    return {client: ls}

def create_client_root_folder():
    # get home
    name = "{0}/{1}".format("Home","Clients")
    frappe.errprint("creating root %s" % name)
    frappe.errprint(frappe.db.sql("select name from tabFile where name = '%s'" % name))
    if not frappe.db.exists("File", name):
        file = frappe.get_doc({
            "doctype": "File",
            "file_name": "Clients",
            "is_folder": 1,
            "folder": "Home"
        })

        file.save(ignore_permissions=True)
        frappe.db.commit()
        return file.name

    return  name

def create_new_folder(file_name, folder, user):
    name = "{0}/{1}".format(folder,file_name)
    frappe.errprint("creating %s" % name)
    frappe.errprint(frappe.db.sql("select name from tabFile where name = '%s'" % name))

    if not frappe.db.exists("File", name):
        file = frappe.get_doc({
            "doctype": "File",
            "file_name": file_name,
            "is_folder": 1,
            "folder": folder
        })

        file.save(ignore_permissions=True)
        frappe.db.commit()

        # share file with customer user
        share_file_with_customer_user(file, user)


def share_file_with_customer_user(file, user, notify=0):

    frappe.errprint("sharing %s with %s" % (file.name, user))
    share.add(file.doctype, file.name, user=user, read=1, write=1, share=0, everyone=0,
              flags=None, notify=notify)


def create_customer_user(customer):
    email = customer.email
    fullname = customer.full_name

    frappe.errprint("creating customer user %s" % email)
    if email is None or frappe.db.exists("User", email):
        return

    user = frappe.get_doc({
        "doctype": "User",
        "user_type": "System User",
        "email": email,
        "send_welcome_email": 1,
        "first_name": fullname or email.split("@")[0]
    })
    user.add_roles('File User')
    user.save(ignore_permissions=True)

@frappe.whitelist()
def update_all(customer, trigger=""):
    try:
        create_customer_user(customer)
        update_customer_folder_structure(customer)
    except Exception as err:
        frappe.errprint(err)



@frappe.whitelist()
def append_permission(doc, trigger=""):
    frappe.errprint("doc  %s" % doc.__dict__)
    users = []
    docshares = share.get_users("File",doc.folder)
    frappe.errprint("docshares  %s" % docshares)

    for docshare in docshares:
        frappe.errprint("attempt to share with  %s" % docshare.user)
        try:
            users.index(docshare.user)
        except ValueError:
            users.append(docshare.user)
            share_file_with_customer_user(doc, docshare.user, 1)
