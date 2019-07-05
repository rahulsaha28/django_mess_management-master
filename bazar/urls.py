from django.urls import path
from bazar.views import (
    bazar_request_sent,
    edit_bazar_for_manager,
    delete_bazar_for_manager
)
urlpatterns = [
    path("", bazar_request_sent, name="pollbazar.pge"),
    path("edit/bazar/",  edit_bazar_for_manager, name="bazar_edit_manager.page"),
    path("delete/bazar/", delete_bazar_for_manager, name="bazar_delete_manager.page"),
]

