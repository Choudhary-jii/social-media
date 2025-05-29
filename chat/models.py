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



class MasterClass(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.id)

class Group(MasterClass):
    name = models.CharField(max_length=255)
    profile_photo = models.ImageField(upload_to='group_photos/', blank=True, null=True)
    creator = models.ForeignKey(CustomUser, related_name='created_groups', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class GroupMember(MasterClass):
    group = models.ForeignKey(Group, related_name='memberships', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='group_memberships', on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)  # NEW FIELD

    class Meta:
        # unique_together = ('group', 'user')
        ordering = ['date_joined']

    def __str__(self):
        role = 'Admin' if self.is_admin else 'Member'
        return f"{self.user} in {self.group} - {'Admin' if self.is_admin else 'Member'}"

class GroupMessage(MasterClass):
    group = models.ForeignKey(Group, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, related_name='group_messages_sent', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    sender_align_right = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        preview = self.content[:20] + ('...' if len(self.content) > 20 else '')
        return f"{self.sender} in {self.group}: {self.content[:20]}"
    






# class MasterClass(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     is_active = models.BooleanField(default=True)

#     class Meta:
#         abstract = True

#     def __str__(self):
#         return self.id

# class Group(MasterClass):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=255)
#     profile_photo = models.ImageField(upload_to='group_photos/', blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     creator = models.ForeignKey(CustomUser, related_name='created_groups', on_delete=models.CASCADE)

#     def __str__(self):
#         return self.name


# class GroupMember(models.Model):
#     group = models.ForeignKey(Group, related_name='memberships', on_delete=models.CASCADE)
#     user = models.ForeignKey(CustomUser, related_name='group_memberships', on_delete=models.CASCADE)
#     is_admin = models.BooleanField(default=False)  # admin flag

#     class Meta:
#         unique_together = ('group', 'user')

#     def __str__(self):
#         return f"{self.user} in {self.group} - {'Admin' if self.is_admin else 'Member'}"


# class GroupMessage(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     group = models.ForeignKey(Group, related_name='messages', on_delete=models.CASCADE)
#     sender = models.ForeignKey(CustomUser, related_name='group_messages_sent', on_delete=models.CASCADE)
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#     is_read = models.BooleanField(default=False)
#     # Boolean for alignment in frontend: True = sender aligned right, False = left
#     sender_align_right = models.BooleanField(default=True)

#     class Meta:
#         ordering = ['timestamp']

#     def __str__(self):
#         return f"{self.sender} in {self.group}: {self.content[:20]}"


