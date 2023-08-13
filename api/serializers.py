from rest_framework import serializers
from .models import User, FriendList, FriendRequest, Notification


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'is_superuser', 'date_joined', 'first_name',
                  'last_name', 'email', 'password', 'surname']


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'surname']


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
