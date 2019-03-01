from __future__ import unicode_literals
from frappe import _


def get_data():
    return [{
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
