from django.db import models

# Create your models here.
import uuid
from django.db import models
from core.models import CustomUser  # import your user model

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(CustomUser, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name="received_messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']  # messages come in order

    def __str__(self):
        return f"{self.sender} ➡️ {self.receiver}: {self.content[:20]}"
