from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(read_only=True)   # Show sender username (or __str__)
    receiver = serializers.StringRelatedField(read_only=True) # Show receiver username (or __str__)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp', 'is_read']
        read_only_fields = ['id', 'timestamp', 'is_read']
