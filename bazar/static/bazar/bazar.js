$(document).ready(function () {

    var edit_bazar_modal = null
    var bazar_cancel = null
    var cancel_bazar_button = null
    var delete_bazar_modal = null
    var i = 0

    $(".edit_bazar_m").on("click", function () {
        if (i == 0) {
            edit_bazar_modal = $(this).parent().children(".edit_bazar_model_m")
            bazar_cancel = $(this).parent().children().children().children(".bazar_cancel_b")
            i += 1
        }
        $(edit_bazar_modal).modal("setting", "closable", false).modal("show")
        $(bazar_cancel).on("click", function () {
            location.reload()
        })
    })

    $(".bazar_delete_button_b").on("click", function(){
        if(i==0){
            delete_bazar_modal = $(this).parent().children(".bazar_delete_modal_b")
            cancel_bazar_button = $(this).parent().children().children().children(".bazar_cancel_b")
            i+=1
        }
        $(delete_bazar_modal).modal("setting", "closable", false).modal("show")
        $(cancel_bazar_button).on("click", function(){
            location.reload()
        })
    })

    $("input[name='date_created']").datepicker({
        format: "dd/mm/yyyy",
        autoHide: true
    })

})