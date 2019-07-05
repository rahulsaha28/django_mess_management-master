from django.urls import path
from notification.views import (
    show_specific_notify,
    delete_specific_notify,
    approve_specific_notify
)
urlpatterns = [
    path("", show_specific_notify, name="showspecificnotify.page"),
    path("delete/", delete_specific_notify, name="deletespecificnotify.page"),
    path("approve/", approve_specific_notify, name="approvespecificnotify.page"),
]