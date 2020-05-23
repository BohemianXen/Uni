from django.contrib import admin
from .models import User, Action, Device

# Allow admins to alter user account details, possible actions, and registered devices through admin site
admin.site.register(User)
admin.site.register(Action)
admin.site.register(Device)
