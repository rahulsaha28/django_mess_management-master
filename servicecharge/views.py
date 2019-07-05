from django.http import HttpResponse
from django.shortcuts import render
from poll.views import PollSetUp
from servicecharge.forms import ServiceForm
from django.contrib import messages
from poll.custome_date import Date
from servicecharge.models import ServiceCharge
from member.models import Member


# Create your views here.
def service_charge_save(request):
    if request.method == "POST":
        service_form = ServiceForm(request.POST)
        content = PollSetUp().for_poll_setting(poll_id=request.POST["poll_id"], user=request.user)
        if service_form.is_valid():
            try:
                service_charge = ServiceCharge.objects.create(
                    service_name=service_form.cleaned_data["service_name"],
                    poll=content["poll"],
                    debit_tk=service_form.cleaned_data["debit_tk"],
                    date=Date().human_to_cp(request.POST["date_created"])
                )
                for member_id in request.POST.getlist("member"):
                    member = Member.objects.get(id=member_id)
                    service_charge.member.add(member)

                messages.add_message(request, level=messages.SUCCESS, message="Successfully created",
                                     extra_tags="negative")
                return render(request, "poll/poll_setting.html", content)

            except:
                messages.add_message(request, level=messages.ERROR, message="Can not created Service Charge.")

        else:
            messages.add_message(request, level=messages.ERROR, message="Something wrong happen.")
            return render(request, "poll/poll_setting.html", content)


# edit the service charge
def edit_service_charge(request):
    if request.method == "POST":
        service_charge = ServiceCharge.objects.get(id=request.POST["servicecharge_id"])
        content = PollSetUp().for_get_manager_poll(poll_id=request.POST["poll_id"])
        members_id = request.POST.getlist("member", False)
        members = []
        if members_id:
            for member_id in members_id:
                members.append(Member.objects.get(id=int(member_id)))
        else:
            print(members)
            members = service_charge.member.all()
        if (service_charge.service_name != request.POST["service_name"]
                or service_charge.debit_tk != request.POST["debit_tk"]
                or service_charge.date != Date().human_to_cp(request.POST["date"])
                or request.POST.getlist("member", False)):
            service_charge.service_name = request.POST["service_name"]
            service_charge.debit_tk = float(request.POST["debit_tk"])
            service_charge.date = Date().human_to_cp(request.POST["date"])
            service_charge.save()
            service_charge.member.clear()
            for member in members:
                service_charge.member.add(member)
            messages.add_message(request, level=messages.SUCCESS, message="Successfully Edited.", extra_tags="success")
        else:
            messages.add_message(request, level=messages.ERROR, message="Nothing Edited", extra_tags="negative")
        return render(request, "poll/manager_poll.html", content)


# This is the delete service charge
def delete_service_charge(request):
    if request.method == "POST":
        content = PollSetUp().for_get_manager_poll(poll_id=request.POST["poll_id"])
        try:
            servicecharge = ServiceCharge.objects.get(id=request.POST["service_id"])
            servicecharge.delete()
            messages.add_message(request, level=messages.SUCCESS, message="Successfully deleted your Service charge",
                                 extra_tags="success")
        except:
            messages.add_message(request, level=messages.ERROR, message="Some error happen", extra_tags="negative")
        return render(request, "poll/manager_poll.html", content)
