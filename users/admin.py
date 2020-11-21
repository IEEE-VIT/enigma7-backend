from django.contrib import admin

from .models import User, UserOutreach, UserStatus, Logging

admin.site.register(User)
admin.site.register(UserStatus)
admin.site.register(Logging)
admin.site.register(UserOutreach)
