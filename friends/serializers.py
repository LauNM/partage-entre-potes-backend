from rest_framework import serializers
from users.serializers import UserListSerializer
from .models import FriendList, FriendRequest, Notification


class FriendRequestSerializer(serializers.ModelSerializer):
    sender = serializers.UUIDField()
    receiver = serializers.UUIDField()

    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'receiver', 'created_at']


class FriendListSerializer(serializers.ModelSerializer):
    friends = UserListSerializer(many=True)

    class Meta:
        model = FriendList
        fields = ['friends']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"

