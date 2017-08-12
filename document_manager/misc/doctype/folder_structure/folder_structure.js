// Copyright (c) 2017, masonarmani and contributors
// For license information, please see license.txt

frappe.ui.form.on('Folder Structure', {
	refresh: function(frm) {
		console.log(frm);
	}
});

frappe.ui.form.on('Folder Structure Item', {
	is_root: function(frm) {
		if (frm.doc.is_root == 1){
			frm.toggle_reqd("parent_folder");
			frm.toggle_enable("parent_folder",1);
		}
	}
});

