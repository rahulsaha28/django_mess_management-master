from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from member.forms import (
    SignUpForm,
    LogInForm,
)
from member.models import Member, Profile, Friend
from notification.models import Notification
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required


# Create your views here.

def home_view(request):
    return render(request, "member/home.html")


# Sign_Up

def signup_view(request):
    if request.method == "POST":
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            member = Member.objects.create_member(email=signup_form.cleaned_data["email"])
            member.set_password(signup_form.cleaned_data["password"])
            member.save()
            Profile.objects.create(member=member)
            messages.add_message(request, level=messages.SUCCESS, message="Successfully created your account.",
                                 extra_tags="success")
            return redirect("home.page")

        else:
            content = {
                'form': signup_form
            }
            return render(request, "member/signup/signup.html", content)


    else:
        signup_form = SignUpForm()
        content = {
            "form": signup_form
        }
        return render(request, "member/signup/signup.html", content)


def login_view(request):
    if request.method == "POST":
        login_form = LogInForm(request.POST)
        if login_form.is_valid():
            member = authenticate(request, email=login_form.cleaned_data["email"],
                                  password=login_form.cleaned_data["password"])
            if member is not None:
                login(request, member)
                return redirect("profile.page")
            else:
                messages.add_message(request, level=messages.ERROR,
                                     message="%s has no valid account." % (login_form.cleaned_data["email"]),
                                     extra_tags="negative")
                return redirect("home.page")

        else:
            content = {
                "form": login_form
            }
            return render(request, "member/login/login.html", content)
    else:
        login_form = LogInForm()
        content = {
            "form": login_form
        }
        return render(request, "member/login/login.html", content)


# logout view
def logout_view(request):
    logout(request)
    return redirect("login.page")


# profile
@login_required(login_url="/login/")
def profile_view(request):
    notifivation = Notification.objects.filter(notification=request.user.profile)
    content = {
        'notification': notifivation
    }

    return render(request, "member/profile/profile.html", content)


@login_required(login_url="/login/")
def find_friend_view(request):
    if request.method == "POST":
        try:
            member = Member.objects.get(email=request.POST["findemail"])
            content = {
                "member": member
            }
            friend = Friend.objects.filter(profile=request.user.profile, member_one=member,
                                           status=False)
            friend1 = Friend.objects.filter(profile=member.profile, member_one=request.user,
                                            status=False)
            friend2 = Friend.objects.filter(profile=request.user.profile, member_one=member,
                                            status=True)
            friend3 = Friend.objects.filter(profile=member.profile, member_one=request.user,
                                            status=True)
            if friend.count() > 0:
                content["sentrequest"] = 1
                return render(request, "member/profile/search_result.html", content)
            elif friend1.count() > 0:
                content["sentrequest"] = 2
                return render(request, "member/profile/search_result.html", content)
            elif friend2.count() > 0 or friend3.count() > 0:
                content["sentrequest"] = 3
                return render(request, "member/profile/search_result.html", content)
            else:
                content["sentrequest"] = 0
                return render(request, "member/profile/search_result.html", content)

        except:
            messages.add_message(request, level=messages.ERROR, message="This Member does not exist.",
                                 extra_tags="negative")
            return redirect("profile.page")


@login_required(login_url="/login/")
def friend_request(request):
    if request.method == "POST":
        member = Member.objects.get(id=request.POST["friend_id"])
        profile = Profile.objects.get(member=request.user)
        friend = Friend()
        friend.profile = profile
        friend.member_one = member
        friend.save()
        Notification.objects.create(
            notification=member.profile,
            from_member=profile.member,
            status="fr",
            m_id=friend.id
        )
        return HttpResponse(json.dumps({'id': member.id}), content_type="application/json")


@login_required(login_url="/login/")
def cancel_friend_request(request):
    if request.method == "POST":
        member = Member.objects.get(id=request.POST["friend_id"])
        friend = Friend.objects.filter(profile=request.user.profile, member_one=member, status=False)
        id = friend[0].member_one.id
        notification = Notification.objects.filter(notification=member.profile, from_member=request.user)
        friend[0].delete()
        notification.delete()
        return HttpResponse(json.dumps({"id": id}), content_type="application/json")


@login_required(login_url="/login/")
def delete_friend_request(request):
    if request.method == "POST":
        profile = Profile.objects.get(member_id=request.POST["friend_id"])
        friend = Friend.objects.filter(profile=profile, member_one=request.user, status=False)
        notification = Notification.objects.filter(notification=request.user.profile, from_member=profile.member)
        friend.delete()
        notification.delete()
        return HttpResponse(json.dumps({"id": request.POST["friend_id"]}), content_type="application/json")


@login_required(login_url="/login/")
def accept_friend_request(request):
    if request.method == "POST":
        profile = Profile.objects.get(member_id=request.POST["friend_id"])
        friend = Friend.objects.filter(profile=profile, member_one=request.user, status=False)[0]
        notification = Notification.objects.filter(notification=request.user.profile, from_member=profile.member)
        friend.status = True
        friend.save()
        notification.delete()
        return HttpResponse(json.dumps({"id": request.POST["friend_id"]}), content_type="application/json")


@login_required(login_url="/login/")
def show_all_friend(request):
    if request.user.is_authenticated:
        friends = Friend.objects.filter(Q(profile=request.user.profile) | Q(member_one=request.user), status=True)
        content = {
            "friends": friends,
        }
        return render(request, "member/profile/all_friends.html", content)


@login_required(login_url="/login/")
def delete_friend(request):
    if request.method == "POST":
        friend = Friend.objects.get(id=request.POST["id"])
        friend.delete()
        return HttpResponse()
