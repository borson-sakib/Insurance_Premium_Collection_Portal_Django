from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.

# class UseAdmin(UserAdmin):
#     pass

admin.site.register(Transaction)
admin.site.register(User)
