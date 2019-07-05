from django.http import HttpResponse
from django.shortcuts import render
from poll.views import PollSetUp
from meal.forms import MealForm
from meal.models import Meal, DefaultMeal, EditedMeal
from notification.models import Notification
from member.models import Member
from poll.models import Poll
from django.utils import timezone
from django.contrib import messages



# Create your views here.
def meal_form_save(request):
    if request.method == "POST":
        content = PollSetUp().for_poll_setting(poll_id=request.POST["poll_id"], user=request.user, is_true=True)
        meal_form = MealForm(request.POST)
        if meal_form.is_valid():
            poll = Poll.objects.get(id=request.POST["poll_id"])
            try:
                DefaultMeal.objects.create(poll=poll,
                                           b=meal_form.cleaned_data["brake_fast"],
                                           l=meal_form.cleaned_data["lunch"],
                                           d=meal_form.cleaned_data["dinner"]
                                           )

                messages.add_message(request, level=messages.SUCCESS, message="Successfully set the meal",
                                     extra_tags="success")
                content["form"] = MealForm()
                return render(request, "poll/poll_setting.html", content)
            except:
                messages.add_message(request, level=messages.ERROR, message="Already exist.", extra_tags="negative")
                content["form"] = MealForm()
                return render(request, "poll/poll_setting.html", content)
        else:
            content["form"] = meal_form
            return render(request, "poll/poll_setting.html", content)


'''
This is the default_meal edit function
'''


def edit_default_meal(request):
    if request.method == "POST":
        if float(request.POST["b"]) < 0 or float(request.POST["l"]) < 0 or float(request.POST["d"]) < 0:
            messages.add_message(request, level=messages.ERROR, message="Meal can not be less than 0")
        else:

            default_meal = DefaultMeal.objects.get(id=int(request.POST["default_meal_id"]))
            default_meal.b = float(request.POST["b"])
            default_meal.l = float(request.POST["l"])
            default_meal.d = float(request.POST["d"])
            default_meal.save()
            messages.add_message(request, level=messages.SUCCESS, message="Your Default Meal is Edited.", extra_tags="success")
        content = PollSetUp().for_poll_setting(poll_id=request.POST["poll_id"], user=request.user)
        return render(request, "poll/poll_setting.html", content)


# meal show for manager
def meal_edit_for_manager(request):
    if request.method == "POST":
        content = PollSetUp().for_get_manager_poll(poll_id=request.POST["poll_id"])
        if request.user.email == content["poll"].manager:
            meal = Meal.objects.get(id=request.POST["meal_id"])
            meal.b = float(request.POST["b"])
            meal.l = float(request.POST["l"])
            meal.d = float(request.POST["d"])
            meal.save()
            messages.add_message(request, level=messages.SUCCESS, message=f"Successfully edited meal of member: {meal.member.email}", extra_tags="success")
        else:
            messages.add_message(request, level=messages.ERROR, message="You are not manager", extra_tags="negative")
        return render(request, "poll/manager_poll.html", content)

def edit_meal_member(request):
    if request.method == "POST":
        content = PollSetUp().for_get_member_poll(user=request.user, poll_id=request.POST["poll_id"])
        meal = content["poll"].meal_set.get(id=request.POST["meal_id"])
        meal.pending = True
        meal.save()
        editmeal = EditedMeal.objects.create(
            meal=meal,
            b=float(request.POST["b"]),
            l=float(request.POST["l"]),
            d=float(request.POST["d"])
        )
        Notification.objects.create(
            notification=Member.objects.get(email=meal.poll.manager).profile,
            from_member=request.user,
            status="ed",
            m_id= editmeal.id,
        )
        messages.add_message(request, level=messages.SUCCESS, message="Successfully sent the Edition.", extra_tags="success")
        return render(request, "poll/member_poll.html", content)