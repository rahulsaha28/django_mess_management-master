from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from member.managers import MemberManager
from django.utils import timezone


# Create your models here.
class Member(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = MemberManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):

        if self.first_name and self.last_name:
            return "%s %s" % (self.first_name, self.last_name)

        else:
            return self.email

    def get_short_name(self):

        if self.first_name:
            return self.first_name
        else:
            return self.email

    def sent_email_member(self, subject, message, from_email, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)



class Profile(models.Model):
    member = models.OneToOneField(Member,on_delete=models.CASCADE)

    def __str__(self):
        return self.member.email


class Friend(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    member_one = models.ForeignKey(Member, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        return "%s sent friend request %s"%(self.profile.member.email, self.member_one.email)

