'''
This is the member_management system
-------------------------------------
1. meal
2. service charge
3.  bazar cost
4. amount = service_charge - bazar_cost
'''

import datetime
from meal.models import DefaultMeal, Meal
from poll.models import Poll
from member.models import Member
from bazar.models import Bazar
from servicecharge.models import ServiceCharge


class ManagerManagement(object):
    def __init__(self, member):
        self.member = member
        self.date = datetime.datetime.now().date()
        self.polls = self._get_poll()
        self.totalMeal = None
        self.totalMember = None
        self.defaultMeal = None

    def set_meal(self):
        if self.polls != None:
            for poll in self.polls:
                try:
                    self.defaultMeal = DefaultMeal.objects.get(poll=poll)
                except:
                    self.defaultMeal = None
            if self.defaultMeal:
                self.totalMember = poll.member.all()
            if self.totalMember:
                for member in self.totalMember:
                    self.totalMeal = member.meal_set.filter(poll=poll, date_of_creation__lte=self.date).order_by(
                        "-date_of_creation")
                    if self.totalMeal.count() > 0:
                        if self.totalMeal[0].date_of_creation >= self.date:
                            continue
                        elif self.totalMeal[0].date_of_creation < self.date:
                            i = 1
                            start_date_get = self.totalMeal[0].date_of_creation + datetime.timedelta(days=i)
                            while start_date_get <= self.date and start_date_get <= poll.end_date:
                                Meal.objects.create(
                                    poll=poll,
                                    member=member,
                                    b=self.defaultMeal.b,
                                    l=self.defaultMeal.l,
                                    d=self.defaultMeal.d,
                                    date_of_creation=start_date_get
                                )
                                i += i
                                start_date_get = start_date_get + datetime.timedelta(days=i)

                    else:
                        i = 0
                        start_date_get = poll.start_date
                        while (poll.start_date <= self.date) and (self.date <= poll.end_date):
                            if start_date_get <= self.date:

                                Meal.objects.create(
                                    poll=poll,
                                    member=member,
                                    b=self.defaultMeal.b,
                                    l=self.defaultMeal.l,
                                    d=self.defaultMeal.d,
                                    date_of_creation=start_date_get
                                )
                                i = 1

                                start_date_get = start_date_get + datetime.timedelta(days=i)

                            else:
                                break

    def _get_poll(self):
        polls = self.member.poll_set.filter(start_date__lte=self.date, end_date__gte=self.date)
        if polls.count() > 0:
            return polls
        else:
            return None


'''
1. total_meal
2. total_bazar
2. total_service_charge
3. debit_tk = (total_meal*meal_rate)+total_service_charge
4. credit_tk = total_bazar
5. balance = debit_tk - credit_tk
'''


class MemberManagememt(object):
    def __init__(self, member):
        self.member = member
        self.polls = []

    def set_polls(self):
        polls = Poll.objects.filter(
            member=self.member
        ).order_by("-start_date")
        for poll in polls:
            p = PollManagement(poll, self.member)
            p.set_meal_rate()
            p.set_total_meal()
            p.set_total_bazar()
            p.set_total_service_charge()
            p.set_credit_cart()
            p.set_debit_cart()
            p.set_balance()
            self.polls.append(p)


class PollManagement(object):
    def __init__(self, poll, member):
        self.member = member
        self.poll = poll
        self.meal_rate = 0
        self.total_meal = 0
        self.total_bazar_cost = 0
        self.total_service_charge = 0
        self.debit_tk = 0
        self.credit_tk = 0
        self.balance = 0

    def set_meal_rate(self):
        totalMeal = 0
        totalBazar = 0
        meals = Meal.objects.filter(
            poll=self.poll
        )
        bazars = Bazar.objects.filter(
            poll=self.poll,
            activate=True
        )
        for meal in meals:
            totalMeal += meal.b + meal.l + meal.d
        for bazar in bazars:
            totalBazar += bazar.cradit_tk

        if totalMeal == 0:
            self.meal_rate = 0
        else:
            self.meal_rate = totalBazar / totalMeal

    def set_total_meal(self):
        meals = Meal.objects.filter(
            poll=self.poll,
            member=self.member
        )
        for meal in meals:
            self.total_meal += meal.b + meal.l + meal.d

    def set_total_bazar(self):
        bazars = Bazar.objects.filter(
            poll=self.poll,
            member=self.member,
            activate=True
        )
        for bazar in bazars:
            self.total_bazar_cost += bazar.cradit_tk

    def set_total_service_charge(self):
        services = ServiceCharge.objects.filter(
            poll=self.poll,
            member=self.member
        )
        for service in services:
            self.total_service_charge += service.debit_tk / service.member.all().count()

    def set_debit_cart(self):
        self.debit_tk = (self.meal_rate * self.total_meal) + self.total_service_charge

    def set_credit_cart(self):
        self.credit_tk = self.total_bazar_cost

    def set_balance(self):
        self.balance = self.debit_tk - self.credit_tk
