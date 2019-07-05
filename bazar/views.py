from django.shortcuts import render
from django.http import HttpResponse
from poll.views import PollSetUp
from bazar.forms import BazarForm
from django.contrib import  messages
from bazar.models import Bazar
from poll.models import Poll
from notification.models import Notification
from member.models import Member
from poll.custome_date import Date

# Create your views here.
def bazar_request_sent(request):
    if request.method == "POST":
        content = PollSetUp().for_poll_home(user=request.user)
        content["bazarform"] = BazarForm()
        content["poll_id"] = request.POST["poll_id"]
        bazar_form = BazarForm(request.POST)
        if bazar_form.is_valid():
            poll = Poll.objects.get(id=content["poll_id"])
            bazar = Bazar.objects.create(
                poll=poll,
                member=request.user,
                cradit_tk=bazar_form.cleaned_data["cradit_tk"],
                date_created= Date().human_to_cp(date=request.POST["date"])

            )
            notify = Notification.objects.create(
                notification= Member.objects.get(email=poll.manager).profile,
                from_member=request.user,
                status="baz",
                date=Date().human_to_cp(date=request.POST["date"]),
                m_id=bazar.id

            )
            messages.add_message(request, level=messages.SUCCESS, message="Sent message to the manager", extra_tags="success")
        else:
            messages.add_message(request, level=messages.ERROR, message="Bazar cost must be positive." , extra_tags="negative")
        print(bazar_form)
        return render(request, "poll/member_poll.html", content)


# edit for manager
def edit_bazar_for_manager(request):
    if request.method == "POST":
        content = PollSetUp().for_get_manager_poll(poll_id=request.POST["poll_id"])
        if request.user.email == content["poll"].manager:
            bazar = content["poll"].bazar_set.get(id=request.POST["bazar_id"])
            bazar.date_created = Date().human_to_cp(date=request.POST["date_created"])
            bazar.cradit_tk = float(request.POST["cradit_tk"])
            bazar.save()
            messages.add_message(request, level=messages.SUCCESS, message=f"Successfully edited bazar for member: {bazar.member.email}.", extra_tags="success")
        else:
            messages.add_message(request, level=messages.ERROR, message="You are not manager.", extra_tags="negative")
        return render(request, 'poll/manager_poll.html', content)


# delete for manager
def delete_bazar_for_manager(request):
    if request.method == "POST":
        content = PollSetUp().for_get_manager_poll(poll_id=request.POST["poll_id"])
        if request.user.email == content["poll"].manager:
            content["poll"].bazar_set.get(id=request.POST["bazar_id"]).delete()
            messages.add_message(request, level=messages.SUCCESS, message="Successfully deleted.", extra_tags="success")
        else:
            messages.add_message(request, level=messages.ERROR, message="You are not Manager.", extra_tags="negative")
    return render(request, "poll/manager_poll.html", content)