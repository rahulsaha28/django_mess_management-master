from django.db import models
from member.models import Member


# Create your models here.
class Poll(models.Model):
    member = models.ManyToManyField(Member)
    poll_name = models.CharField(max_length=30)
    manager = models.EmailField(max_length=254)
    start_date = models.DateField(auto_now_add=False)
    end_date = models.DateField(auto_now_add=False)

    def __str__(self):
        return f"{self.poll_name} started at {self.start_date} and end at {self.end_date}"
