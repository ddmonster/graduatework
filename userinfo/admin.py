from django.contrib import admin

# Register your models here.
from userinfo.models import *
admin.site.register(UserInfo)
admin.site.register(Adress)