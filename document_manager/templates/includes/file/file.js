frappe.ready(function () {
    $(".struct-wrapper").on("click",".struct a._", function (rb) {
        rb.preventDefault();
        var _this = rb.target.parentElement;
        var href = $(this).attr('href');
        _this.classList.toggle("active", !_this.classList.contains("active"));
        _this.classList.toggle("not-active", _this.classList.contains("not-active"));
        if (!_this.classList.contains("loaded")) {
            $.ajax({
                method: "GET",
                url: "/",
                data: {
                    cmd: "document_manager.www.documents._get_children",
                    name: href
                },
                dataType: "json",
                success: function (data) {
                    // generate struct item
                    if (data.message != undefined) {
                        var lis = "";
                        data.message.forEach(function (v) {
                            if(v.is_folder){
                                lis += "<li class='struct' tabindex='1'> <a href='"+v.old_parent+"/"+v.file_name
                                    +"' class='_'></a><span>" + v.file_name + "</span></li>"
                            }else{
                                lis += "<li class='struct-file' tabindex='1'><span class='icon'></span>" + v.file_name
                                    + " <a href='"+v.file_url+"' class='preview'> download</a></li> "
                            }
                        });
                        var struc_item = `<ul class="struct-items">${lis}</ul>`;
                        _this.innerHTML += struc_item;
                    }
                    _this.classList.add("loaded");
                }
            })
        }
    })
})