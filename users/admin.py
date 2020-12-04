from django.contrib import admin

from .models import User, UserOutreach, UserStatus, Logging

admin.site.register(UserStatus)
admin.site.register(UserOutreach)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'question_id', 'points', 'xp')
    search_fields = ('email', 'username')
    ordering = (('points'), )


@admin.register(Logging)
class LogginAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'answer', 'timestamp')
    search_fields = ('user__username', 'answer')
    ordering = (('timestamp'), )
