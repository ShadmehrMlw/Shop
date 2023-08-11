from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm
from .models import User, OtpCode
# Register your models here.

@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'created')

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'phone_number', 'is_active', 'is_admin')
    list_filter = ('is_admin',)
    readonly_fields = ('last_login',)

    fieldsets = (
        ('Main', {'fields':('email', 'phone_number', 'password')}),
        ('Permission', {'fields':('is_active', 'is_admin', 'last_login')}),
    )

    add_fieldsets = (
        ('None', {'fields':('email', 'phone_number', 'full_name', 'password1', 'password2', 'is_admin')}),
    )

    search_fields = ('phone_number',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.unregister(Group)
admin.site.register(User, UserAdmin)

