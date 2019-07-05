from django.contrib import admin
from meal.models import Meal, DefaultMeal, EditedMeal
# Register your models here.
admin.site.register(Meal)
admin.site.register(DefaultMeal)
admin.site.register(EditedMeal)