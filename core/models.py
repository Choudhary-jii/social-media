import os
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    bio = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)

    followers = models.ManyToManyField("self", symmetrical=False, related_name="following", blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name']

    objects = CustomUserManager()

    def __str__(self):
        return self.username
    

def user_directory_path(instance, filename):
    # instance is a Post instance
    # store images in media/{user_uuid}/filename
    return os.path.join(str(instance.user.id), filename)


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, related_name="posts", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/')
    description = models.TextField(blank=True)
    likes = models.ManyToManyField(CustomUser, related_name="liked_posts", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def likes_count(self):
        return self.likes.count()

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

