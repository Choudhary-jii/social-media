from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommentViewSet, UserViewSet, PostViewSet

router = DefaultRouter()
router.register('user', UserViewSet, basename='user')
router.register('posts', PostViewSet, basename='post')
router.register('comments', CommentViewSet, basename='comment')


urlpatterns = [
    path('', include(router.urls)),
]