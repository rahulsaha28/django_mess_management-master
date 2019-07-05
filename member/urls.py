from django.urls import path, include
from member.views import (
    home_view,
    signup_view,
    login_view,
    logout_view,
    profile_view,
    find_friend_view,
    friend_request,
    cancel_friend_request,
    show_all_friend,
    delete_friend_request,
    accept_friend_request,
    delete_friend
)

urlpatterns = [
    path("", home_view, name="home.page"),
    path("signup/", signup_view, name="signup.page"),
    path("login/", login_view, name="login.page"),
    path("logout/", logout_view, name="logout.page"),
    path("profile/", profile_view, name="profile.page"),
    # search_for_friend
    path("friend/search/", find_friend_view, name="findfriend.page"),
    path("friend/request/", friend_request, name="friendrequest.page"),
    path("friend/request/cancel/", cancel_friend_request, name="friendrequestcancel.page"),
    path("friend/request/delete/", delete_friend_request, name="friendrequestdelete.page"),
    path("friend/request/accept/", accept_friend_request, name="friendrequestaccept.page"),

    # show_all_friend
    path("friend/all/", show_all_friend, name="showallfriend.page"),
    path("friend/delete/", delete_friend, name="deletefriend.page"),

    # for poll
    path("poll/", include("poll.urls")),

    # for meal
    path("meal/", include("meal.urls")),
    path("service/", include("servicecharge.urls")),

    # for bazar
    path("bazar/", include("bazar.urls")),

    # Notify
    path("notification/", include("notification.urls"))
]
