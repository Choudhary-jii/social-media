from django.contrib import admin
from .models import Message, Group, GroupMember, GroupMessage


class GroupMemberInline(admin.TabularInline):
    model = GroupMember
    extra = 0
    readonly_fields = ('date_joined', 'created_at', 'updated_at')


class GroupMessageInline(admin.TabularInline):
    model = GroupMessage
    extra = 0
    readonly_fields = ('timestamp', 'created_at', 'updated_at')
    
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'content', 'timestamp', 'is_read')
    search_fields = ('sender__username', 'receiver__username', 'content')
    list_filter = ('is_read', 'timestamp')
    readonly_fields = ('timestamp',)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'created_at', 'is_active')
    search_fields = ('name', 'creator__username')
    list_filter = ('created_at', 'is_active')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [GroupMemberInline, GroupMessageInline]

@admin.register(GroupMember)
class GroupMemberAdmin(admin.ModelAdmin):
    list_display = ('group', 'user', 'is_admin', 'date_joined', 'is_active')
    search_fields = ('group__name', 'user__username')
    list_filter = ('is_admin', 'date_joined', 'is_active')
    readonly_fields = ('date_joined', 'created_at', 'updated_at')

@admin.register(GroupMessage)
class GroupMessageAdmin(admin.ModelAdmin):
    list_display = ('group', 'sender', 'content', 'timestamp', 'is_read', 'sender_align_right', 'is_active')
    search_fields = ('group__name', 'sender__username', 'content')
    list_filter = ('timestamp', 'is_read', 'sender_align_right', 'is_active')
    readonly_fields = ('timestamp', 'created_at', 'updated_at')



