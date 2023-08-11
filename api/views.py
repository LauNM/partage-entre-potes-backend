from .models import Product, Category, User, FriendList, FriendRequest
from .serializers import (ProductSerializer, CategorySerializer, UserSerializer,
                          UserListSerializer, FriendListSerializer, FriendRequestSerializer)
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminAuthenticated
from django.db.models import Q

"""
ADMIN
"""


class AdminUserViewset(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAdminAuthenticated]

    queryset = User.objects.all()


class AdminProductViewset(ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminAuthenticated]

    queryset = Product.objects.all()


class AdminFriendRequestViewset(ModelViewSet):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAdminAuthenticated]

    queryset = FriendRequest.objects.all()


class AdminFriendListViewset(ModelViewSet):
    serializer_class = FriendListSerializer
    permission_classes = [IsAdminAuthenticated]

    queryset = FriendList.objects.all()


"""
USER
"""


class UserViewset(ModelViewSet):
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()


class ProductViewset(ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        user = self.request.user
        return Product.objects.filter(owner=user)


class CategoryViewset(ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    queryset = Category.objects.all()


class FriendListViewset(ModelViewSet):
    serializer_class = FriendListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return FriendList.objects.filter(user=user)


class FriendRequestViewset(ModelViewSet):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(Q(sender=user) | Q(receiver=user) & Q(is_active=True))



