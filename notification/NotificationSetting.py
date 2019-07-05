from member.models import Friend
from poll.models import Poll
from bazar.models import Bazar
from meal.models import Meal, EditedMeal


class NotificationProcessing(object):
    def __init__(self, notification):
        self.notification = notification

    def for_delete_notification(self):
        if self.notification.get_status_display() == "friend":
            Friend.objects.get(id=self.notification.m_id).delete()
            self.notification.delete()
            return True
        elif self.notification.get_status_display() == "poll_member_request":
            self.notification.delete()
            return True
        elif self.notification.get_status_display() == "bazar_cost":
            Bazar.objects.get(id=self.notification.m_id).delete()
            self.notification.delete()
            return True
        elif self.notification.get_status_display() == "edit":
            ed = EditedMeal.objects.get(id=self.notification.m_id)
            meal = ed.meal
            meal.pending = False
            meal.save()
            ed.delete()
            self.notification.delete()
            return True
        else:
            return False

    def for_approve_notification(self):
        if self.notification.get_status_display() == "friend":
            friend = Friend.objects.get(id=self.notification.m_id)
            friend.status = True
            friend.save()
            self.notification.delete()
            return True
        elif self.notification.get_status_display() == "poll_member_request":
            member = self.notification.notification.member
            Poll.objects.get(id=self.notification.m_id).member.add(member)
            self.notification.delete()
            return True
        elif self.notification.get_status_display() == "bazar_cost":
            bazar = Bazar.objects.get(id=self.notification.m_id)
            bazar.activate = True
            bazar.save()
            self.notification.delete()
            return True
        elif self.notification.get_status_display() == "edit":
            ed = EditedMeal.objects.get(id=self.notification.m_id)
            meal = ed.meal
            if ed.b != meal.b:
                meal.b = ed.b
            if ed.l != meal.l:
                meal.l = ed.l
            if ed.d != meal.d:
                meal.d = ed.d
            meal.pending = False
            meal.save()
            ed.delete()
            self.notification.delete()
            return True
        else:
            return False