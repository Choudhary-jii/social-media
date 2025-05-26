# from django.urls import path
# from .views import MessageListCreateView, GroupListView, GroupCreateView, GroupDetailUpdateView, GroupDetailView, GroupMessageListCreateView

# urlpatterns = [
#     path('messages/', MessageListCreateView.as_view(), name='messages-list-create'),
#     path('groups/', GroupListView.as_view(), name='group-list-view'),
#     path('groups/', GroupCreateView.as_view(), name='group-list-create'),
#     path('groups/', GroupDetailUpdateView.as_view(), name='group-list-update'),
#     path('group-details/<uuid:pk>/', GroupDetailView.as_view(), name='group-detail'),
#     path('group-messages/', GroupMessageListCreateView.as_view(), name='group-messages'),
# ]

from django.urls import path
from .views import (
    MessageListCreateView,
    GroupListView,
    GroupCreateView,
    GroupDetailUpdateView,
    GroupDetailView,
    GroupMessageListCreateView,
)

urlpatterns = [
    path('messages/', MessageListCreateView.as_view(), name='messages-list-create'),

    # Separate list and create routes for groups
    path('groups/', GroupListView.as_view(), name='group-list'),                  # GET all groups
    path('groups/create/', GroupCreateView.as_view(), name='group-create'),       # POST to create a group
    path('groups/<uuid:id>/', GroupDetailUpdateView.as_view(), name='group-update'),  # GET, PUT, PATCH (update)

    # Group detail for admin actions (GET, PUT/PATCH, DELETE with admin permission)
    path('group-details/<uuid:pk>/', GroupDetailView.as_view(), name='group-detail'),

    # Group messages
    path('group-messages/', GroupMessageListCreateView.as_view(), name='group-messages'),
]
