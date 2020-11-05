from django.contrib import admin

from .models import User, UserStatus, Logging

admin.site.register(User)
admin.site.register(UserStatus)
admin.site.register(Logging)
