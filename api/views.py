from .models import Product, Category, User, FriendList, FriendRequest
from .serializers import (ProductSerializer, CategorySerializer, UserSerializer,
                          UserListSerializer, FriendListSerializer, FriendRequestSerializer)
from .models import User, FriendList, FriendRequest
from .models import Notification
from products.models import Product, Reservation
from .serializers import (UserSerializer, UserListSerializer, FriendListSerializer, FriendRequestSerializer)
from products.serializers import ProductSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .permissions import IsAdminAuthenticated
from django.db.models import Q

"""
ADMIN VIEWSET
"""


class AdminUserViewset(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAdminAuthenticated]

    queryset = User.objects.all()


class AdminFriendRequestViewset(ModelViewSet):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAdminAuthenticated]

    queryset = FriendRequest.objects.all()


class AdminFriendListViewset(ModelViewSet):
    serializer_class = FriendListSerializer
    permission_classes = [IsAdminAuthenticated]

    queryset = FriendList.objects.all()


"""
USER VIEWSET
"""


class UserViewset(ModelViewSet):
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()


"""
FRIEND VIEWSET
"""


class FriendListProductViewset(ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        friends = FriendList.objects.get(user=user).friends.all()
        products = Product.objects.filter(owner__in=friends)

        owner = self.request.query_params.get('owner')
        if owner:
            products = products.filter(owner=owner)

        status = self.request.query_params.get('status')
        if status:
            products = products.filter(status=status)

        category = self.request.query_params.get('category')
        if category:
            products = products.filter(category=category)

        return products

    @action(detail=True, methods=['post'])
    def request_reservation(self, request, pk=None):
        product = self.get_object()  # Obtient le produit concerné
        user = request.user

        if product.status != 'AVAILABLE':
            return Response({'message': 'Product is not available for reservation'}, status=status.HTTP_400_BAD_REQUEST)

class CategoryViewset(ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
        Reservation.objects.create(product=product, user=user)
        product.status = 'BOOKED'
        product.save()

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
        return FriendRequest.objects.filter(Q(sender=user) | Q(receiver=user))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sender = request.user
        receiver_id = serializer.validated_data['receiver']
        receiver = User.objects.get(id=receiver_id)

        if sender == receiver:
            return Response({"detail": "You cannot send a friend request to yourself."}, status=status.HTTP_400_BAD_REQUEST)

        existing_request = FriendRequest.objects.filter(sender=sender, receiver=receiver, is_active=True).first()
        if existing_request:
            return Response({"detail": "A friend request to this user is already active."}, status=status.HTTP_400_BAD_REQUEST)

        friend_request = FriendRequest(sender=sender, receiver=receiver)
        friend_request.save()

        return Response({"detail": "Friend request sent successfully."}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.sender != request.user and instance.receiver != request.user:
            return Response({"detail": "You do not have permission to delete this friend request."}, status=status.HTTP_403_FORBIDDEN)

        instance.delete()

        return Response({"detail": "Friend request deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        friend_request = self.get_object()

        if friend_request.receiver != request.user:
            return Response({"detail": "You do not have permission to accept this friend request."},
                            status=status.HTTP_403_FORBIDDEN)

        friend_request.accept()

        return Response({"detail": "Friend request accepted successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def decline(self, request, pk=None):
        friend_request = self.get_object()

        if friend_request.receiver != request.user:
            return Response({"detail": "You do not have permission to decline this friend request."},
                            status=status.HTTP_403_FORBIDDEN)

        friend_request.decline()

        return Response({"detail": "Friend request declined successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        friend_request = self.get_object()

        if friend_request.sender != request.user:
            return Response({"detail": "You do not have permission to cancel this friend request."},
                            status=status.HTTP_403_FORBIDDEN)

        friend_request.cancel()

        return Response({"detail": "Friend request canceled successfully."}, status=status.HTTP_200_OK)