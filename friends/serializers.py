from rest_framework import serializers
from users.serializers import UserListSerializer
from .models import FriendList, FriendRequest, Notification


class FriendRequestSerializer(serializers.ModelSerializer):
    # sender = UserListSerializer(many=False)
    # receiver = UserListSerializer(many=False)

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
        field = "__all__"

