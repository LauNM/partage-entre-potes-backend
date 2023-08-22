from rest_framework import serializers
from users.serializers import UserListSerializer
from .models import Product, Category, Reservation


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

    def validate_name(self, value):
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError('Category already exists')
        return value


class CategoryField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        category = Category.objects.get(pk=value.pk)
        return {
            'id': category.id,
            'name': category.name
        }


class ProductSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display', read_only=True)
    category = CategoryField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'date_created', 'date_updated', 'status', 'category', 'owner', 'image']


class ProductField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        product = Product.objects.get(pk=value.pk)
        return {
            'id': product.id,
            'name': product.name,
            'owner_id': product.owner.id,
            'owner_surname': product.owner.surname,
            'status': product.status
        }


class ReservationSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display', read_only=True)
    product = ProductField(queryset=Product.objects.all())

    class Meta:
        model = Reservation
        fields = ['id', 'product', 'requester', 'status', 'created_at']

