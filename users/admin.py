from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('phone_number', 'invite_code', 'invited_by')
    ordering = ('phone_number', )