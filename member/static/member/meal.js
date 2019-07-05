$(document).ready(function () {
    var edit_meal = null
    var cancel_meal = null
    var j = 0
    $(".edit_meal_e").on("click", function () {
        if (j == 0) {
            edit_meal = $(this).parent().children(".edit_meal_detail")
            cancel_meal = $(this).parent().children().children().children(".cancel_meal_x")
            console.log(cancel_meal)
        }
        $(edit_meal).modal("show")

        $(cancel_meal).on("click", function () {
            location.reload()
        })
    })
})