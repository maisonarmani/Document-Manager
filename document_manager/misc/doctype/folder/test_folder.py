# -*- coding: utf-8 -*-
# Copyright (c) 2017, masonarmani and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import unittest


class TestFolder(unittest.TestCase):
    pass


def get_structure():
    client = "Maison Armani"
    structure = "Simple Client"

    def get_children(structure, parent):
        ls = frappe.db.sql("select fsi.child from `tabFolder Structure` fs inner join `tabFolder Structure Item` fsi "
                           "where (fsi.parent = fs.name) and (fs.name = '{structure}')  and parent_folder='{parent}'"
                           .format(structure=structure, parent=parent), as_list=1)

        return [x[0] for x in ls]

    ls = {}
    for v in get_children(structure, "Root"):
        _ = get_children(structure, v)
        if _ == []:
            x = v
        else:
            x = _
        ls.update({ v: x })

    return { client : ls}

