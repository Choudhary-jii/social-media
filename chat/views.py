from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied, NotFound, ValidationError
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction, models

from .models import Message, Group, GroupMember, GroupMessage
from .serializers import (
    MessageSerializer,
    GroupSerializer,
    GroupMessageSerializer,
)
from core.models import CustomUser

User = CustomUser

class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        other_user_id = self.request.query_params.get('user')

        if not other_user_id:
            return Message.objects.none()

        try:
            other_user = User.objects.get(id=other_user_id)
        except User.DoesNotExist:
            return Message.objects.none()

        return Message.objects.filter(
            (models.Q(sender=user) & models.Q(receiver=other_user)) |
            (models.Q(sender=other_user) & models.Q(receiver=user))
        ).order_by('timestamp')

    def perform_create(self, serializer):
        receiver_id = self.request.data.get('receiver')
        if not receiver_id:
            raise PermissionDenied("Receiver is required")
        try:
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            raise PermissionDenied("Receiver does not exist")
        serializer.save(sender=self.request.user, receiver=receiver)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class IsGroupMemberPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return GroupMember.objects.filter(group=obj, user=request.user).exists()


class IsGroupAdminPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return GroupMember.objects.filter(group=obj, user=request.user, is_admin=True).exists()


# class GroupListCreateView(generics.ListCreateAPIView):
#     serializer_class = GroupSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return Group.objects.filter(memberships__user=self.request.user).distinct()

#     @transaction.atomic
#     def perform_create(self, serializer):
#         creator = self.request.user
#         group = serializer.save(creator=creator)

#         # Add creator as admin (serializer already handled most, this ensures it)
#         GroupMember.objects.update_or_create(
#             group=group, user=creator, defaults={'is_admin': True}
#         )


# 1. List View (GET all groups for current user)
class GroupListView(generics.ListAPIView):
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Group.objects.filter(memberships__user=self.request.user).distinct()


# 2. Create View (POST to create a group)
class GroupCreateView(generics.CreateAPIView):
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def perform_create(self, serializer):
        creator = self.request.user
        group = serializer.save()

        # Ensure creator is saved as admin
        GroupMember.objects.update_or_create(
            group=group, user=creator, defaults={'is_admin': True}
        )


# 3. Detail + Update View (GET, PUT, PATCH for single group)
class GroupDetailUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Group.objects.all()
    lookup_field = 'id'  # if you're using UUIDs

    def get_queryset(self):
        # User must be a member of the group to access
        return Group.objects.filter(memberships__user=self.request.user).distinct()


class GroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated, IsGroupMemberPermission]
    queryset = Group.objects.all()

    def check_admin_permission(self, group):
        user = self.request.user
        if not GroupMember.objects.filter(group=group, user=user, is_admin=True).exists():
            raise PermissionDenied("You must be an admin to perform this action")

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        group = self.get_object()
        self.check_admin_permission(group)

        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(group, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        members_data = request.data.get('members', None)
        self.perform_update(serializer)

        if members_data is not None:
            creator = group.creator
            GroupMember.objects.filter(group=group).exclude(user=creator).delete()

            for member in members_data:
                user_data = member.get('user')
                if not user_data:
                    continue
                user_id = user_data.get('id')
                if not user_id or str(user_id) == str(creator.id):
                    continue

                try:
                    user = CustomUser.objects.get(id=user_id)
                except CustomUser.DoesNotExist:
                    raise ValidationError(f"User with id {user_id} does not exist")

                is_admin = member.get('is_admin', False)
                GroupMember.objects.create(group=group, user=user, is_admin=is_admin)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        group = self.get_object()
        self.check_admin_permission(group)
        return super().destroy(request, *args, **kwargs)


class GroupMessageListCreateView(generics.ListCreateAPIView):
    serializer_class = GroupMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        group_id = self.request.query_params.get('group')
        if not group_id:
            return GroupMessage.objects.none()

        group = get_object_or_404(Group, id=group_id)

        if not GroupMember.objects.filter(group=group, user=self.request.user).exists():
            raise PermissionDenied("You are not a member of this group")

        return GroupMessage.objects.filter(group=group).order_by('timestamp')

    # def perform_create(self, serializer):
    #     group_id = self.request.data.get('group_id')
    #     if not group_id:
    #         raise ValidationError("group_id is required")

    #     group = get_object_or_404(Group, id=group_id)

    #     if not GroupMember.objects.filter(group=group, user=self.request.user).exists():
    #         raise PermissionDenied("You are not a member of this group")

    #     serializer.save(sender=self.request.user, group=group, sender_align_right=True)

    def perform_create(self, serializer):
        group_id = self.request.data.get('group_id')
        if not group_id:
            raise ValidationError("group_id is required")

        group = get_object_or_404(Group, id=group_id)

        if not GroupMember.objects.filter(group=group, user=self.request.user).exists():
            raise PermissionDenied("You are not a member of this group")

        # Don't pass 'group' here — the serializer will handle it with 'group_id'
        serializer.save(sender=self.request.user, sender_align_right=True)


