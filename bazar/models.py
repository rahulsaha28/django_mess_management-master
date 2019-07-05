from django.db import models
from poll.models import Poll
from member.models import Member


# Create your models here.
class Bazar(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    cradit_tk = models.FloatField(default=0)
    activate = models.BooleanField(default=False)
    date_created = models.DateField(auto_now_add=False)

    def __str__(self):
        return f"{self.member.email} is bazar for {self.poll.poll_name}."
