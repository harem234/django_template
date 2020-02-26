from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from user.forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth import get_user_model


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (_('extended'), {'fields': ('site', 'is_email_verified',)}),
    )

    # change
    custom_add_fieldsets = UserAdmin.add_fieldsets
    # create
    custom_add_fieldsets[0][1]['fields'] = ('email', 'password1', 'password2')
    add_fieldsets = custom_add_fieldsets + (
        (_('extended'), {'fields': ('site', 'is_email_verified',)}),
    )
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = list(UserAdmin.list_display + ('site', 'site_id',))
    list_display.remove('username')
    list_display = tuple(list_display)
    search_fields = ('email', 'first_name', 'last_name',)
    ordering = ('email',)


admin.site.register(get_user_model(), CustomUserAdmin)
