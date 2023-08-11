from rest_framework import serializers
from .models import Product, Category, User, FriendList, FriendRequest


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
    sender = UserListSerializer(many=False)
    receiver = UserListSerializer(many=False)

    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'receiver', 'created_at']


class FriendListSerializer(serializers.ModelSerializer):
    friends = UserListSerializer(many=True)

    class Meta:
        model = FriendList
        fields = ['friends']


class ProductSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'date_created', 'date_updated', 'status', 'category', 'owner', 'image']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

    def validate_name(self, value):
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError('Category already exists')
        return value

