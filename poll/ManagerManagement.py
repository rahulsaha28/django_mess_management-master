'''
--------------------------------------------------------------------------------
1. Member
    >total meal
    >meal rate
    >total bazar
    >total service charge
    >credit tk = total bazar
    >debit tk = (total meal*meal rate)+total service charge
    >balance
2. Poll
    >Member
    > meal rate = ( totalBazar / totalMeal)

--------------------------------------------------------------------------------

'''
from poll.models import Poll
from meal.models import Meal
from bazar.models import Bazar
from servicecharge.models import ServiceCharge


class MessMember(object):
    # constructor method
    def __init__(self, member):
        # instance variable
        self.member = member
        self.total_meal = 0
        self.total_bazar_cost = 0
        self.total_service_charge = 0
        self.credit_tk = 0
        self.debit_tk = 0
        self.balance = 0

    # for set value of each instance variable has a method
    def set_total_meal(self, poll):
        meals = Meal.objects.filter(
            poll=poll,
            member=self.member
        )
        for meal in meals:
            self.total_meal += meal.b + meal.l + meal.d

    def set_total_bazar_cost(self, poll):
        bazars = Bazar.objects.filter(
            poll=poll,
            member=self.member,
            activate=True
        )
        for bazar in bazars:
            self.total_bazar_cost += bazar.cradit_tk

    def set_total_service_charge(self, poll):
        services = ServiceCharge.objects.filter(
            poll=poll,
            member=self.member
        )
        for service in services:
            self.total_service_charge += (service.debit_tk / service.member.all().count())

    def set_credit_tk(self):
        self.credit_tk = self.total_bazar_cost

    def set_debit_tk(self, meal_rate):
        self.debit_tk = (meal_rate*self.total_meal)+self.total_service_charge

    def set_balance(self):
        self.balance = self.debit_tk - self.credit_tk

class MessPoll(object):
    # constructor method
    def __init__(self, poll_id):
        self.poll = Poll.objects.get(id=poll_id)
        self.members = []
        self.meal_rate = 0
        self.totalService = 0
        self.totalBack = 0
        self.calculation_error = 0

    def _add_member_in_poll(self):
        for member in self.poll.member.all():
            self.members.append(MessMember(member=member))

    def _set_all(self):
        for member in self.members:
            member.set_total_meal(self.poll)
            member.set_total_bazar_cost(self.poll)
            member.set_total_service_charge(self.poll)

    # this is the meal rate of a poll
    def _set_meal_rate(self):
        self._add_member_in_poll()
        self._set_all()
        totalBazar = 0
        totalMeal = 0
        for member in self.members:
            totalMeal += member.total_meal
            totalBazar += member.total_bazar_cost
        if totalMeal == 0:
            self.meal_rate = 0
        else:
            self.meal_rate = totalBazar/totalMeal

    def _set_for_all(self):
        self._set_meal_rate()
        for member in self.members:
            member.set_credit_tk()
            member.set_debit_tk(self.meal_rate)
            member.set_balance()

    # set total service in a poll
    def _set_total_service(self):
        services = ServiceCharge.objects.filter(
            poll=self.poll
        )
        for service in services:
            self.totalService += service.debit_tk
    def _set_total_back(self):
        self._set_for_all()
        for member in self.members:
            self.totalBack += member.balance

    def action(self):
        self._set_total_service()
        self._set_total_back()
        self.calculation_error = self.totalService - self.totalBack
