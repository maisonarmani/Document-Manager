from __future__ import unicode_literals
from frappe import _


def get_data():
    return [
        {
            "label": _("Document"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Client",
                    "description": _("Client")
                },
                {
                    "type": "doctype",
                    "name": "File",
                    "label":"Folder",
                    "description": _("Client Documents")
                },
            ]
        },

        {
            "label": _("Setup"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Folder Structure",
                    "description": _("Folder Structure")
                },
                {
                    "type": "doctype",
                    "name": "Folder",
                    "description": _("Folder")
                },
            ]
        }
    ]
