from django.http import HttpResponse
from django.shortcuts import render, redirect
from notification.models import Notification
from notification.NotificationSetting import NotificationProcessing
from django.contrib import messages
from meal.models import EditedMeal

# Create your views here.
def show_specific_notify(request):
    if request.method == "POST":
        content = {
            "notification":Notification.objects.get(id=request.POST["notify_id"])
        }
        if content["notification"].get_status_display() == "edit":
            content["editmeal"] = EditedMeal.objects.get(id=content["notification"].m_id)
        return render(request, "notification/show_notification.html", content)

# Delete the notification
def delete_specific_notify(request):
    if request.method == "POST":
        notify = Notification.objects.get(id=request.POST["notify_id"])
        notify_status = NotificationProcessing(notify).for_delete_notification()
        if notify_status:
            messages.add_message(request, level=messages.SUCCESS, message="Action execute.", extra_tags="success")
        else:
            messages.add_message(request, level=messages.ERROR, message="Error happen!!", extra_tags="negative")
        return redirect("home.page")

# approve notification
def approve_specific_notify(request):
    if request.method =="POST":
        notify = Notification.objects.get(id=request.POST["notify_id"])
        notify_status = NotificationProcessing(notify).for_approve_notification()
        if notify_status:
            messages.add_message(request, level=messages.SUCCESS, message="Action execute.", extra_tags="success")
        else:
            messages.add_message(request, level=messages.ERROR, message="Error happen!!", extra_tags="negative")
        return redirect("home.page")




