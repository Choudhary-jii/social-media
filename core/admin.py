from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Post, Comment

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'name', 'is_active', 'is_staff')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'username', 'name')
    ordering = ('date_joined',)

    fieldsets = (
        (None, {'fields': ('email', 'username', 'name', 'password')}),
        ('Personal Info', {'fields': ('bio', 'phone_number', 'profile_photo')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Relationships', {'fields': ('followers',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'name', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Post)
admin.site.register(Comment)
