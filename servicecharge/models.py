from django.db import models
from poll.models import Poll
from member.models import Member


# Create your models here.
class ServiceCharge(models.Model):
    service_name = models.CharField(max_length=20)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    member = models.ManyToManyField(Member)
    debit_tk = models.FloatField(default=0)
    date = models.DateField(auto_now_add=False)

    def __str__(self):
        return f"{self.service_name} in the poll {self.poll.poll_name}."
