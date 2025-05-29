# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import CustomUser, Post, Comment



# class PostInline(admin.TabularInline):
#     model = Post
#     extra = 0
#     readonly_fields = ('created_at',)

# class CommentInline(admin.TabularInline):
#     model = Comment
#     extra = 0
#     readonly_fields = ('created_at',)



# class CustomUserAdmin(UserAdmin):
#     model = CustomUser
#     list_display = ('email', 'username', 'name', 'followers_count', 'id', 'phone_number', 'is_active', 'is_staff')
#     list_filter = ('is_staff', 'is_active')
#     search_fields = ('email', 'username', 'name', 'phone_number', 'id')
#     # ordering = ('date_joined',)
#     inlines = [PostInline]


#     def followers_count(self, obj):
#         return obj.followers.count()
#     # followers_count.short_description = 'Followers'
#     followers_count.short_description = 'Followers Count'

#     fieldsets = (
#         (None, {'fields': ('email', 'username', 'name', 'password')}),
#         ('Personal Info', {'fields': ('bio', 'phone_number', 'profile_photo')}),
#         # ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         # ('Important dates', {'fields': ('last_login',)}),
#         ('Social Network', {'fields': ('followers',)}),
#     )

#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'username', 'name', 'phone_number', 'password1', 'password2', 'is_active', 'is_staff')}
#         ),
#     )

# # class PostAdmin(admin.ModelAdmin):
# #     model = Post

# #     list_display = ('id', 'user', 'image', 'description', 'likes_count', 'created_at')
# #     list_filter = ('user', 'created_at')
# #     search_fields = ('id', 'user__username', 'description', 'created_at')
# #     inlines = [CommentInline]

# #     @property
# #     def likes_count(self):
# #         return self.likes.count()
# #     # likes_count.short_description = 'likes'
# #     #likes_count.short_description = 'Likes Count'

# #     # fieldsets = (
# #     #     (None, {'fields': ('image', 'description', 'likes_count', 'created_at')}),
# #     #     ('Personal Info', {'fields': ('id', 'user')}),
# #     #     ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
# #     # )
# #     fieldsets = (
# #     (None, {'fields': ('user', 'image', 'description')}),
# #     ('Meta', {'fields': ('created_at',)}),
# #     )
# #     readonly_fields = ('created_at', 'likes_count',)
# #     list_display = ('id', 'user', 'image', 'description', 'likes_count', 'created_at')
    



# #     add_fieldsets = ((None, {'classes': ('wide',), 'fields': ('user', 'image', 'description')}),)

# class PostAdmin(admin.ModelAdmin):
#     model = Post

#     list_display = ('id', 'user', 'image', 'description', 'likes_count', 'created_at')
#     list_filter = ('user', 'created_at')
#     search_fields = ('id', 'user__username', 'description', 'created_at')
#     inlines = [CommentInline]

#     def likes_count(self, obj):
#         return obj.likes.count()
#     likes_count.short_description = 'Likes Count'

#     fieldsets = (
#         (None, {'fields': ('user', 'image', 'description')}),
#         ('Meta', {'fields': ('created_at',)}),
#     )
#     readonly_fields = ('created_at', 'likes_count')

#     add_fieldsets = (
#         (None, {'classes': ('wide',), 'fields': ('user', 'image', 'description')}),
#     )



# class CommentAdmin(admin.ModelAdmin):
#     model = Comment

#     list_display = ('id', 'user', 'post', 'content', 'created_at')
#     list_filter = ('user', 'post', 'content', 'created_at')
#     search_fields = ('id', 'user', 'post', 'content', 'created_at')
    
#     fieldsets = ((None, {'fields': ('user', 'post', 'content')}),)

    
# admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(Post, PostAdmin)
# admin.site.register(Comment, CommentAdmin)



from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Post, Comment


class PostInline(admin.TabularInline):
    model = Post
    extra = 0
    readonly_fields = ('created_at',)


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('created_at',)


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'name', 'followers_count', 'id', 'phone_number', 'is_active', 'is_staff')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'username', 'name', 'phone_number', 'id')
    inlines = [PostInline]

    def followers_count(self, obj):
        return obj.followers.count()
    followers_count.short_description = 'Followers Count'

    fieldsets = (
        (None, {'fields': ('email', 'username', 'name', 'password')}),
        ('Personal Info', {'fields': ('bio', 'phone_number', 'profile_photo')}),
        ('Social Network', {'fields': ('followers',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'name', 'phone_number', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )


class PostAdmin(admin.ModelAdmin):
    model = Post

    def likes_count(self, obj):
        return obj.likes.count()
    likes_count.short_description = 'Likes Count'

    list_display = ('id', 'user', 'image', 'description', 'likes_count', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('id', 'user__username', 'description', 'created_at')
    inlines = [CommentInline]

    fieldsets = (
        (None, {'fields': ('user', 'image', 'description')}),
        ('Meta', {'fields': ('created_at',)}),
    )
    readonly_fields = ('created_at',)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user', 'image', 'description')}
        ),
    )


class CommentAdmin(admin.ModelAdmin):
    model = Comment

    list_display = ('id', 'user', 'post', 'content', 'created_at')
    list_filter = ('user', 'post', 'content', 'created_at')
    search_fields = ('id', 'user__username', 'post__id', 'content', 'created_at')

    fieldsets = (
        (None, {'fields': ('user', 'post', 'content')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
