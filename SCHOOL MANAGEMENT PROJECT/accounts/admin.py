from django.contrib import admin
from .models import CustomUser, School
from django.contrib.auth.admin import UserAdmin


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('role', 'school')}),
    )

admin.site.register(School)