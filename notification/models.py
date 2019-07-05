from django.db import models
from member.models import Profile, Member

# Create your models here.
class Notification(models.Model):
    status_all = [
        ('fr',"friend"),
        ('ed', "edit"),
        ('po', "poll_member_request"),
        ("baz", "bazar_cost"),
    ]
    notification = models.ForeignKey(Profile, on_delete=models.CASCADE)
    from_member = models.ForeignKey(Member, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=status_all)
    m_id = models.IntegerField(default=-1, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s notification for %s"%(self.get_status_display(), self.notification.member.email)