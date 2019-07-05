$(document).ready(function () {

    var edit_meal_sent = null
    var cancel_meal_sent = null
    var i = 0

    $(".edit_meal_sent_m").on("click", function () {
        if (i == 0) {
            edit_meal_sent = $(this).parent().children(".edit_meal_modal_m")
            cancel_meal_sent = $(this).parent().children().children().children(".cancel_meal_sent_m")
            i += 1
        }
        $(edit_meal_sent).modal("setting", "closable", false).modal("show")
        $(cancel_meal_sent).on("click", function () {
            location.reload()
        })
    })

})