from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from accounts.forms import UserForm, CustomUserChangeForm
# from core.models import Review
# from core.models import Camp

# Register your models here.

User = get_user_model()

# ModelAdmin


class CustomUserAdmin(UserAdmin):
    add_form = UserForm
    form = CustomUserChangeForm
    model = User
    add_fieldsets = (
        ('Personal Details', {'fields': ('email', 'full_name', 'picture', 'password1', 'password2')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Optional', {'fields': ('bio','mobile','address','city')}),
        )
    fieldsets = (
        ('Personal Details', {'fields': ('email', 'full_name', 'picture')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Optional', {'fields': ('bio','mobile','address','city')}),
        )
    
    ordering = ('email',)
    list_display=['email', 'full_name','is_staff']





admin.site.register(User,CustomUserAdmin)