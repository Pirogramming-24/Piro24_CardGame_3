from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.urls import reverse
from django.utils.html import format_html

from .models import Profile

# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user_link", "nickname")
    search_fields = ("nickname", "user__username", "user__email")

    def user_link(self, obj):
        url = reverse("admin:auth_user_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)

    user_link.short_description = "User"

class UserAdmin(BaseUserAdmin):
    list_display = BaseUserAdmin.list_display + ("profile_link",)

    def profile_link(self, obj):
        if not hasattr(obj, "profile"):
            return "-"

        app_label = Profile._meta.app_label
        model_name = Profile._meta.model_name
        url = reverse(f"admin:{app_label}_{model_name}_change", args=[obj.profile.id])
        return format_html('<a href="{}">Profile</a>', url)

    profile_link.short_description = "Profile"


admin.site.unregister(User)
admin.site.register(User, UserAdmin)