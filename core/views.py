from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .models import CustomUser
from .serializers import UserRegisterSerializer, UserDetailSerializer, UserUpdateSerializer
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema


from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Post
from .serializers import PostSerializer, PostCreateUpdateSerializer
from rest_framework.exceptions import PermissionDenied


from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from .models import Comment
from .serializers import CommentSerializer, PostCommentCreateSerializer


class UserPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserViewSet(viewsets.ViewSet):
    """
    Handles register, retrieve, update, delete profile.
    """
    lookup_field = 'id'
    queryset = CustomUser.objects.all()

    @extend_schema(
        request=UserRegisterSerializer,
        responses={201: {'message': 'User registered successfully'}, 400: 'Validation error'}
    )
    def create(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @extend_schema(
        responses={200: UserDetailSerializer, 404: {'error': 'User not found'}}
    )     
    def retrieve(self, request, pk=None):
        try:
            user = CustomUser.objects.get(id=pk)
            serializer = UserDetailSerializer(user)
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        request=UserUpdateSerializer,
        responses={200: {'message': 'Profile updated successfully'}, 400: 'Validation error'},
    )
    @action(detail=False, methods=['put'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile updated successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        responses={200: {'message': 'Profile deleted successfully'}, 401: 'Unauthorized'},
    )
    @action(detail=False, methods=['delete'], permission_classes=[IsAuthenticated])
    def delete_profile(self, request):
        user = request.user
        user.delete()
        return Response({'message': 'Profile deleted successfully'})


    @extend_schema(
        responses={200: UserDetailSerializer(many=True)}
    )
    def list(self, request):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=401)

        if not request.user.is_staff:
            return Response({'detail': 'You do not have permission to perform this action.'}, status=403)

        users = CustomUser.objects.all().order_by('id')
        paginator = UserPagination()
        page = paginator.paginate_queryset(users, request)
        if page is not None:
            serializer = UserDetailSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = UserDetailSerializer(users, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def follow(self, request, id=None):
        target_user = get_object_or_404(CustomUser, id=id)
        if target_user == request.user:
            return Response({'error': "You can't follow yourself."}, status=400)

        target_user.followers.add(request.user)
        return Response({'message': f'You are now following {target_user.username}'}, status=200)


    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unfollow(self, request, id=None):
        target_user = get_object_or_404(CustomUser, id=id)
        if target_user == request.user:
            return Response({'error': "You can't unfollow yourself."}, status=400)

        target_user.followers.remove(request.user)
        return Response({'message': f'You have unfollowed {target_user.username}'}, status=200)
    

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def followers(self, request, id=None):
        user = get_object_or_404(CustomUser, id=id)
        followers = user.followers.all()
        serializer = UserDetailSerializer(followers, many=True)
        return Response(serializer.data, status=200)


    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def following(self, request, id=None):
        user = get_object_or_404(CustomUser, id=id)
        following = user.following.all()
        serializer = UserDetailSerializer(following, many=True)
        return Response(serializer.data, status=200)


class PostViewSet(viewsets.ModelViewSet):
    """
    Handles creating, listing, retrieving, updating, deleting posts,
    and liking/unliking them.
    """
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = UserPagination  # Use your existing pagination class

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PostCreateUpdateSerializer
        return PostSerializer

    def list(self, request, *args, **kwargs):
        user = request.user

        if user.is_staff:
            # Admin: see all posts
            queryset = Post.objects.all().order_by('-created_at')
        else:
            # Normal user: see only their own posts
            queryset = Post.objects.filter(user=user).order_by('-created_at')

        # queryset = self.filter_queryset(self.get_queryset())

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        post = self.get_object()
        if post.user != self.request.user:
            raise PermissionDenied("You can only update your own posts.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You can only delete your own posts.")
        instance.delete()

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def toggle_like(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        user = request.user

        if user in post.likes.all():
            post.likes.remove(user)
            return Response({'detail': 'Post unliked'}, status=status.HTTP_200_OK)
        else:
            post.likes.add(user)
            return Response({'detail': 'Post liked'}, status=status.HTTP_200_OK)
        

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PostCommentCreateSerializer
        return CommentSerializer

    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
 
    def perform_update(self, serializer):
        comment = self.get_object()
        if comment.user != self.request.user:
            raise PermissionDenied("You can only update your own comments.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You can only delete your own comments.")
        instance.delete()