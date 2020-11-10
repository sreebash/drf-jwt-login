from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from .forms import UserCreationForm

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm

    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_admin', 'is_staff')
    list_display_links = ('email', 'first_name', 'last_name')
    list_filter = ('is_admin',)
    fieldsets = ('email',)


admin.site.unregister(Group)
admin.site.register(User)
