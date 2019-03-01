# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version
from frappe import _

app_name = "document_manager"
app_title = "Document Manager"
app_publisher = "masonarmani"
app_description = "This is to manage documents"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "masonarmani38@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/document_manager/css/document_manager.css"
# app_include_js = "/assets/document_manager/js/document_manager.js"

# include js, css files in header of web template
# web_include_css = "/assets/document_manager/css/document_manager.css"
# web_include_js = "/assets/document_manager/js/document_manager.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "document_manager.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
#website_generators = ["File"]


# treeviews = ['Folder Structure']
# Installation
# ------------

# before_install = "document_manager.install.before_install"
# after_install = "document_manager.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "document_manager.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways


#permission_query_conditions = {
 	#"File": "document_manager.document_manager.doctype.client.client.get_permission_query_conditions_for_file",
#}

#standard_portal_menu_items = [
#	{"title": _("Document Manager"), "route": "/documents", "reference_doctype": "File"}
#]
# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "File": {
        "after_save":"document_manager.client.share_file_with_customer_user"
#       "after_save": "method"
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
    },
    "Customer": {
        "on_update": "document_manager.client.update_all"
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"document_manager.tasks.all"
# 	],
# 	"daily": [
# 		"document_manager.tasks.daily"
# 	],
# 	"hourly": [
# 		"document_manager.tasks.hourly"
# 	],
# 	"weekly": [
# 		"document_manager.tasks.weekly"
# 	]
# 	"monthly": [
# 		"document_manager.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "document_manager.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "document_manager.event.get_events"
# }

