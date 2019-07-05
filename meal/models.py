from django.db import models
from poll.models import Poll
from member.models import Member


# Create your models here.
class Meal(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    b = models.FloatField(default=0)
    l = models.FloatField(default=0)
    d = models.FloatField(default=0)
    pending = models.BooleanField(default=False)
    date_of_creation = models.DateField(auto_now_add=False)

    def __str__(self):
        return f"{self.poll.poll_name} meal for {self.member.email} at {self.date_of_creation}"


# Create the model for default meal
class DefaultMeal(models.Model):
    poll = models.OneToOneField(Poll, on_delete=models.CASCADE)
    b = models.FloatField(default=0)
    l = models.FloatField(default=0)
    d = models.FloatField(default=0)

    def __str__(self):
        return f"Default meal for {self.poll.poll_name}"


class EditedMeal(models.Model):
    meal = models.OneToOneField(Meal, on_delete=models.CASCADE)
    b = models.FloatField(default=0)
    l = models.FloatField(default=0)
    d = models.FloatField(default=0)

    def __str__(self):
        return f"The edited meal is {self.meal.id}"
