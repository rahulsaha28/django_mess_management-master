from django.shortcuts import render, redirect
from django.http import HttpResponse
from poll.forms import PollForm
from poll.models import Poll
from member.models import Friend, Member
from django.db.models import Q
from django.contrib import messages
from meal.forms import MealForm
from meal.models import DefaultMeal
from servicecharge.forms import ServiceForm
from servicecharge.models import ServiceCharge
from notification.models import Notification
from bazar.forms import BazarForm
from poll.MemberManagement import MemberManagememt, PollManagement
from poll.ManagerManagement import MessPoll

from poll.MemberManagement import ManagerManagement
# Create your views here.

def poll_home(request):
    if request.user.is_authenticated:

        ManagerManagement(request.user).set_meal()
        content = PollSetUp().for_poll_home(request.user)
        return render(request, "poll/home.html", content)


def poll_creation_form(request):
    if request.method == "POST":
        poll_form = PollForm(request.POST)
        content = {
            "form": poll_form
        }
        if poll_form.is_valid():

            poll = Poll(
                poll_name=poll_form.cleaned_data["poll_name"],
                start_date=poll_form.cleaned_data["start_date"],
                manager=request.user.email,
                end_date=poll_form.cleaned_data["end_date"]
            )
            poll.save()
            poll.member.add(request.user)
            return redirect("pollhome.page")

        else:
            return render(request, "poll/poll_form.html", content)
    else:
        poll_form = PollForm()

        content = {
            "form": poll_form
        }
    return render(request, "poll/poll_form.html", content)


def get_manager_poll(request, poll_id):
    content = PollSetUp().for_get_manager_poll(poll_id=poll_id)
    return render(request, "poll/manager_poll.html", content)


# setting
def poll_setting(request):
    content = PollSetUp()
    content = content.for_poll_setting(poll_id=request.POST["poll_id"], user=request.user)
    return render(request, "poll/poll_setting.html", content)


def poll_select_member(request):
    if request.method == "POST":
        content = PollSetUp().for_poll_setting(poll_id=request.POST["poll_id"], user=request.user)
        for member_id in request.POST.getlist("member"):
            member = Member.objects.get(id=member_id)
            poll = Poll.objects.filter(id=request.POST["poll_id"], member=member)

            if poll.count() > 0:
                messages.add_message(request, level=messages.ERROR, message=f"Member {member.email} already exist.",
                                     extra_tags="negative")
                return render(request, "poll/poll_setting.html", content)

        poll = Poll.objects.get(id=request.POST["poll_id"])
        for member_id in request.POST.getlist("member"):
            member = Member.objects.get(id=member_id)
            Notification.objects.create(
                notification=member.profile,
                from_member=request.user,
                status="po",
                m_id=poll.id
            )
        messages.add_message(request, level=messages.SUCCESS, message=f"Poll request for all member sent successfully.",
                             extra_tags="success")
        return render(request, "poll/poll_setting.html", content)


# delete the member form the poll
def delete_member_from_poll(request):
    if request.method == "POST":
        poll = Poll.objects.get(id=request.POST["poll_id"])
        member = Member.objects.get(id=request.POST["member_id"])
        if member.email == request.user.email:
            messages.add_message(request, level=messages.ERROR, message="Manager can't remove himself.",
                                 extra_tags="negative")
        elif poll.manager == request.user.email:
            poll.member.remove(member)
            messages.add_message(request, level=messages.SUCCESS, message=f"Remove the member {member.email}",
                                 extra_tags="success")
        else:
            messages.add_message(request, level=messages.ERROR, message="User is not manager.", extra_tags="negative")

        content = PollSetUp().for_poll_setting(poll_id=request.POST["poll_id"], user=request.user)
        return render(request, "poll/poll_setting.html", content)


# delete the poll
def poll_delete(request):
    if request.method == "POST":
        poll = Poll.objects.get(id=request.POST["poll_id"])
        if request.user.email == poll.manager:
            poll.delete()
            messages.add_message(request, level=messages.SUCCESS, message="Successfully deleted the poll.",
                                 extra_tags="success")
        else:
            messages.add_message(request, level=messages.ERROR, message="You are not manager.", extra_tags="negative")
        poll = Poll.objects.filter(manager=request.user.email)
        content = {
            "polls": poll
        }
        return render(request, "poll/home.html", content)


''''
-----------------------------
This is the member who is not the manager
-----------------------------
'''


def get_member_poll(request, poll_id):
    content = PollSetUp().for_get_member_poll(user=request.user, poll_id=poll_id)
    return render(request, "poll/member_poll.html", content)


# -------------------------------------------------------------------------

# Creating class for Poll set up
class PollSetUp(object):
    def __init__(self):
        self.content = {
            "poll": None,
            "friends": None,
            "form": None,
            "defaultmeal": None,
            "serviceform": None,
            "member_polls": None,
        }

    def for_poll_setting(self, poll_id=None, user=None, is_true=False):
        self.content["poll"] = Poll.objects.get(id=poll_id)
        self.content["friends"] = Friend.objects.filter(Q(profile=user.profile) | Q(member_one=user), status=True)
        self.content["defaultmeal"] = DefaultMeal.objects.filter(poll=self.content["poll"])

        if self.content["poll"].manager == user.email:
            m = MessPoll(self.content["poll"].id)
            m.action()
            self.content["messpoll"] = m
        self.content["serviceform"] = ServiceForm()
        if not is_true:
            self.content["form"] = MealForm()
        return self.content

    def for_get_manager_poll(self, poll_id=None):
        self.content["poll"] = Poll.objects.get(id=poll_id)
        self.content["meals"] = self.content["poll"].meal_set.all().order_by("-date_of_creation")
        self.content["bazars"] = self.content["poll"].bazar_set.filter(activate=True).order_by("-date_created")
        self.content["servicecharges"] = ServiceCharge.objects.filter(poll=self.content["poll"])
        return self.content

    def for_poll_home(self, user):
        self.content["polls"] = Poll.objects.filter(manager=user.email)
        m = MemberManagememt(member=user)
        m.set_polls()
        self.content["member_polls"] = m
        return self.content

    def for_get_member_poll(self, user, poll_id):
        self.for_poll_home(user=user)
        self.content["bazarform"] = BazarForm()
        self.content["poll"] = Poll.objects.get(id=poll_id)
        self.content["meals"] = self.content["poll"].meal_set.filter(member=user).order_by("-date_of_creation")
        self.content["bazars"] = self.content["poll"].bazar_set.filter(member=user, activate=True).order_by(
            "-date_created")
        self.content["servicecharges"] = self.content["poll"].servicecharge_set.filter(member=user).order_by("-date")
        return self.content
