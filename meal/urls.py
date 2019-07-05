from django.urls import path
from meal.views import (
    meal_form_save,
    edit_default_meal,
    meal_edit_for_manager,
    edit_meal_member,
)
urlpatterns = [
    path("save/", meal_form_save, name="mealformsave.page"),
    path("edit/save/", edit_default_meal, name="edit_meal_save.page"),
    path("edit/meal/", meal_edit_for_manager, name="meal_edit_manager.page"),
    path("edit/member/meal/", edit_meal_member, name="edit_by_member.page"),
]