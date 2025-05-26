import json
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Message, Group, GroupMember, GroupMessage
from core.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']  


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(read_only=True)
    receiver = serializers.StringRelatedField(read_only=True)
    is_sender = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp', 'is_read', 'is_sender']
        read_only_fields = ['id', 'timestamp', 'is_read']

    def get_is_sender(self, obj):
        request = self.context.get('request')
        return obj.sender == request.user if request and hasattr(request, 'user') else False


class GroupMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Nested serializer here
    user_id = serializers.UUIDField(write_only=True)
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = GroupMember
        fields = ['user', 'user_id', 'is_admin', 'date_joined']


class GroupSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField(read_only=True)
    # members = GroupMemberSerializer(many=True, source='memberships', required=False)
    members = serializers.SerializerMethodField()
    profile_photo = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'profile_photo', 'created_at', 'creator', 'members']

    def get_members(self, instance):
        members = instance.memberships.all()
        return GroupMemberSerializer(members, many=True).data
    
    def validate(self, attrs):
        members_data = self.initial_data.get('members', [])
        user_ids = [member['user_id'] for member in members_data]
        if len(user_ids) != len(set(user_ids)):
            raise ValidationError("Duplicate users found in members list.")

        # print("Printing Attributes : ", attrs)
        # members = attrs.get('members', [])
        # user_ids = [member['user_id'] for member in members]
        # if len(user_ids) != len(set(user_ids)):
        #     raise serializers.ValidationError("Duplicate users found in members list.")
        return attrs


    def create(self, validated_data):
        members_data = self.initial_data.get('members', [])
        print('members: ', members_data)
        creator = self.context['request'].user
        group = Group.objects.create(creator=creator, **validated_data)
        GroupMember.objects.create(group=group, user=creator, is_admin=True)
        print("Hello coder !")
        # print(json.loads(members_data))
        print(type(members_data))  
        for member_data in members_data:
            print("Inside loop, members data : ", member_data)
            user_id = member_data.get('user_id')
            if user_id != creator.id:
                try:
                    user = CustomUser.objects.get(id=user_id)
                except CustomUser.DoesNotExist:
                    raise ValidationError({'user_id': f'User with id {user_id} does not exist.'})
                GroupMember.objects.create(
                    group=group,
                    user=user,
                    is_admin=member_data.get('is_admin', False)
                )
        return group

    def update(self, instance, validated_data):
        members_data = self.initial_data.get('members', [])
        # members_data = validated_data.pop('members', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if members_data is not None:
            GroupMember.objects.filter(group=instance).exclude(user=instance.creator).delete()
            for member_data in members_data:
                user_id = member_data.get('user_id')
                if user_id != instance.creator.id:
                    try:
                        user = CustomUser.objects.get(id=user_id)
                    except CustomUser.DoesNotExist:
                        raise ValidationError({'user_id': f'User with id {user_id} does not exist.'})
                    GroupMember.objects.create(
                        group=instance,
                        user=user,
                        is_admin=member_data.get('is_admin', False)
                    )

        return instance


class GroupMessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(read_only=True)
    group = serializers.StringRelatedField(read_only=True)
    group_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = GroupMessage
        fields = ['id', 'group', 'group_id', 'sender', 'content', 'timestamp', 'is_read', 'sender_align_right']
        read_only_fields = ['id', 'timestamp', 'is_read', 'sender', 'group']

    def validate(self, attrs):
        user = self.context['request'].user
        group_id = attrs.get('group_id')

        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            raise ValidationError({'group_id': f'Group with id {group_id} does not exist.'})

        if not GroupMember.objects.filter(group=group, user=user).exists():
            raise ValidationError("You are not a member of this group.")

        return attrs
    

    def create(self, validated_data):
        group_id = self.initial_data.get('group_id')
        group = get_object_or_404(Group, id=group_id)
        validated_data['group'] = group
        return super().create(validated_data)
    



    