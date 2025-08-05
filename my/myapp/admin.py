# my/myapp/admin.py
from django.contrib import admin
from .models import Project, ContactMessage
from .models import Project, ContactMessage, Profile, OTPCode

# (your existing admins...)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'headline')

@admin.register(OTPCode)
class OTPCodeAdmin(admin.ModelAdmin):
    list_display = ('phone', 'code', 'created_at', 'is_used')
    readonly_fields = ('token', 'created_at')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    prepopulated_fields = {"slug": ("title",)}

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    readonly_fields = ('name', 'email', 'message', 'created_at')
