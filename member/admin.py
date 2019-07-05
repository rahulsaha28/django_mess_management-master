from django.contrib import admin
from member.models import (
    Member, Profile, Friend
)
# Register your models here.
admin.site.register(Member)
admin.site.register(Profile)
admin.site.register(Friend)
