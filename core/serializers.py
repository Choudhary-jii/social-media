from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Post, Comment

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'name', 'bio', 'phone_number', 'profile_photo']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # Hash the password
        user.save()
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    no_of_followers = serializers.SerializerMethodField()
    no_of_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'bio', 'phone_number', 'profile_photo', 'no_of_followers', 'no_of_following']

    def get_no_of_followers(self, obj):
        return obj.followers.count()

    def get_no_of_following(self, obj):
        return obj.following.count()
    

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'bio', 'phone_number', 'profile_photo']




User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # show username instead of id

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at']


class PostCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post', 'content']


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['image', 'description']


class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # username
    likes_count = serializers.SerializerMethodField()
    liked_by = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'user', 'image', 'description',
            'likes_count', 'liked_by', 'comments',
            'created_at'
        ]

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_liked_by(self, obj):
        return [user.username for user in obj.likes.all()]
