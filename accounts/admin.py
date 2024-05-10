from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserType,UserProfile

class UserTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    filter_horizontal = ['permissions']

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profiles'

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'first_name','last_name', 'user_type', 'is_active', 'is_staff', 'is_completed']
    search_fields = ['email', 'first_name','last_name']
    list_filter = ['user_type', 'is_active', 'is_staff', 'is_completed','is_socialaccount']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name','last_name')}),
        ('Permissions', {'fields': ('user_type', 'is_active', 'is_staff', 'is_superuser', 'is_socialaccount', 'is_completed')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'user_type'),
        }),
    )

    ordering = ['email']
    inlines = [UserProfileInline]

admin.site.register(UserType, UserTypeAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
