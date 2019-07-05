from django.urls import path
from poll.views import (
    poll_creation_form,
    poll_home,
    get_manager_poll,
    poll_setting,
    poll_select_member,
    delete_member_from_poll,
    poll_delete,
    get_member_poll
)

urlpatterns = [
    path("", poll_home, name="pollhome.page"),
    path("create/", poll_creation_form, name="pollform.page"),
    path("<int:poll_id>/", get_manager_poll, name="getcreatedpoll.page"),
    path("setting/", poll_setting ,name="pollsetting.poll"),
    path("setting/selectmember/", poll_select_member ,name="pollselectmenber.poll"),
    path("setting/member/delete/",delete_member_from_poll ,name="pollmemberdelete.page"),
    path("delete/",poll_delete, name="polldelete.page"),
    # This is the member_poll
    path("member_poll/<int:poll_id>/", get_member_poll, name="memberpole.page"),
]

