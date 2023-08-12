from rest_framework import serializers
from api.serializers import UserListSerializer
from .models import Product, Category, Reservation


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

    def validate_name(self, value):
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError('Category already exists')
        return value


class ProductSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display', read_only=True)
    owner = UserListSerializer(many=False)
    category = CategorySerializer(many=False)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'date_created', 'date_updated', 'status', 'category', 'owner', 'image']


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        field = "__all__"

