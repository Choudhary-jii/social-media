from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Message
from .serializers import MessageSerializer
from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()

class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get logged-in user
        user = self.request.user
        
        # Get the 'receiver' user id from query params
        other_user_id = self.request.query_params.get('user')

        if not other_user_id:
            return Message.objects.none()  # no user specified, return empty

        try:
            other_user = User.objects.get(id=other_user_id)
        except User.DoesNotExist:
            return Message.objects.none()

        # Return messages where logged-in user is sender or receiver
        # AND other_user is the other participant
        return Message.objects.filter(
            (models.Q(sender=user) & models.Q(receiver=other_user)) |
            (models.Q(sender=other_user) & models.Q(receiver=user))
        ).order_by('timestamp')

    def perform_create(self, serializer):
        # Set sender as logged-in user
        receiver_id = self.request.data.get('receiver')
        if not receiver_id:
            raise PermissionDenied("Receiver is required")
        try:
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            raise PermissionDenied("Receiver does not exist")

        # Save message with sender=logged in user and receiver
        serializer.save(sender=self.request.user, receiver=receiver)
