from django.urls import path
from servicecharge.views import (
    service_charge_save,
    edit_service_charge,
    delete_service_charge
)
urlpatterns = [
    path("save/", service_charge_save, name="service_charge_save"),
    path("edit/", edit_service_charge, name="edit_service_charge"),
    path("delete/", delete_service_charge, name="delete_service_charge"),

]