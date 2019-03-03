# -*- coding: utf-8 -*-
# Copyright (c) 2017, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import share, _


def update_customer_folder_structure(customer):
    customer_email = customer.get('email')
    if customer_email is None:
        frappe.throw("Please provide customer user for new user")

    root = create_client_root_folder()

    share_file_with_customer_user_str(root, customer_email, notify=0)
    share_file_with_customer_user_str("Home", customer_email, notify=0)

    folders, client_name = [], customer.name
    client_structure = get_structure(structure="Primary", client=client_name)
    folders.append({"parent": root, "folder_name": client_name})
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
            "select fsi.child from `tabFolder Structure` fs inner join `tabFolder Structure Item` fsi limit 1",
            as_list=1)

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
    name = "{0}/{1}".format("Home", "Clients")
    frappe.errprint("creating root %s" % name)
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

    return name


def create_new_folder(file_name, folder, user):
    name = "{0}/{1}".format(folder, file_name)
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

    add_user_icon("File", user, label=file_name, link="List/File/%s"%name, standard=0)


def share_file_with_customer_user(file, user, notify=0):
    name = file.get("name")
    frappe.errprint("sharing %s with %s" % (name, user))
    share.add("File", name, user=user, read=1, write=1, share=0, everyone=0,
              flags=None, notify=notify)


def share_file_with_customer_user_str(file, user, notify=0):
    frappe.errprint("sharing %s with %s" % (file, user))
    share.add("File", file, user=user, read=1, write=1, share=0, everyone=0,
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
        "send_welcome_email": 0,
        "first_name": fullname or email.split("@")[0],
        "block_modules": [{"module": "Buying"}]
    })
    user.add_roles('File User')
    user.insert(ignore_permissions=True)
    user.save(ignore_permissions=True)


    # Block other module view


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
    docshares = share.get_users("File", doc.folder)
    frappe.errprint("docshares  %s" % docshares)

    for docshare in docshares:
        frappe.errprint("attempt to share with  %s" % docshare.user)
        try:
            users.index(docshare.user)
        except ValueError:
            users.append(docshare.user)
            share_file_with_customer_user(doc, docshare.user, 0)


def add_user_icon(_doctype, user, _report=None, label=None, link=None, type='link', standard=0):
    '''Add a new user desktop icon to the desktop'''

    if not label: label = _doctype or _report
    if not link: link = 'List/{0}'.format(_doctype)

    frappe.errprint("attempt to add desktop with  %s" % user)

    # find if a standard icon exists
    icon_name = frappe.db.exists('Desktop Icon', {'standard': standard, 'link': link,
                                                  'owner': user})

    if icon_name:
        if frappe.db.get_value('Desktop Icon', icon_name, 'hidden'):
            # if it is hidden, unhide it
            frappe.db.set_value('Desktop Icon', icon_name, 'hidden', 0)
            clear_desktop_icons_cache()

    else:
        idx = frappe.db.sql('select max(idx) from `tabDesktop Icon` where owner=%s', user)[0][0] or \
              frappe.db.sql('select count(*) from `tabDesktop Icon` where standard=1')[0][0]

        if not frappe.db.get_value("Report", _report):
            _report = None
            userdefined_icon = frappe.db.get_value('DocType', _doctype, ['icon', 'module'], as_dict=True)
        else:
            userdefined_icon = frappe.db.get_value('Report', _report, ['icon', 'module'], as_dict=True)

        module_icon = frappe.get_value('Desktop Icon', {'standard': 1, 'module_name': userdefined_icon.module},
                                       ['name', 'icon', 'color', 'reverse'], as_dict=True)

        if not module_icon:
            module_icon = frappe._dict()
            opts = random.choice(32)
            module_icon.color = opts[0]
            module_icon.reverse = 0 if (len(opts) > 1) else 1

        try:
            new_icon = frappe.get_doc({
                'doctype': 'Desktop Icon',
                'label': label,
                'module_name': label,
                'link': link,
                'type': type,
                '_doctype': _doctype,
                '_report': _report,
                'icon': "octicon-file-directory",
                'color': module_icon.color,
                'reverse': module_icon.reverse,
                'idx': idx + 1,
                'custom': 1,
                'hidden': 0,
                'standard': standard
            })
            new_icon.owner = user
            new_icon.insert(ignore_permissions=True)
            clear_desktop_icons_cache(user)

            icon_name = new_icon.name

        except frappe.UniqueValidationError as e:
            frappe.errprint(_('Desktop Icon already exists %s' % e))

    return icon_name


def get_all_icons():
    return [d.module_name for d in frappe.get_all('Desktop Icon',
                                                  filters={'standard': 1}, fields=['module_name'])]


def clear_desktop_icons_cache(user=None):
    frappe.cache().hdel('desktop_icons', user or frappe.session.user)
    frappe.cache().hdel('bootinfo', user or frappe.session.user)


def get_modules():
    modules = [m.module_name for m in frappe.db.get_all('Desktop Icon',
                  fields=['module_name'], filters={'standard': 1}, order_by="module_name")]

    frappe.errprint("Modules %s", modules)
    return modules

def block(user, module):
    block_module = frappe.db.new_doc({
        "doctype":"Block Module",
        "module":module,
        "owner":user
    })
    frappe.errprint("Blocked modules %s", block_module)
    block_module.insert()


def block_modules_for_user(user):
    for module in get_modules():
        block(module, user)