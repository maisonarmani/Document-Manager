// Copyright (c) 2017, masonarmani38@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Client', {

	setup: (frm) => {
		frm.fields_dict['folder_structure'].get_query = function(doc, cdt, cdn) {
			return {
				filters:{
					is_default: 0,
					enabled:1
				}
			}
		};
	}
});
