from django.contrib import admin

# Register your models here.

from .models import User, Action, Device

admin.site.register(User)
admin.site.register(Action)
admin.site.register(Device)
