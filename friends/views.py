from .models import FriendList, FriendRequest, Notification
from users.models import User
from products.models import Product, Reservation
from .serializers import FriendListSerializer, FriendRequestSerializer, NotificationSerializer
from products.serializers import FriendListProductSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from api.permissions import IsAdminAuthenticated
from django.db.models import Q
from django.utils.translation import gettext as _
from rest_framework import filters
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


"""
ADMIN VIEWSET
"""


class AdminFriendRequestViewset(ModelViewSet):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAdminAuthenticated]

    queryset = FriendRequest.objects.all()


class AdminFriendListViewset(ModelViewSet):
    serializer_class = FriendListSerializer
    permission_classes = [IsAdminAuthenticated]

    queryset = FriendList.objects.all()


class AdminNotificationViewset(ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    queryset = Notification.objects.all()


"""
FRIEND VIEWSET
"""


class FriendListProductViewset(ModelViewSet):
    serializer_class = FriendListProductSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['owner__surname', 'status', 'category']
    search_fields = ['owner__surname', 'name', 'description']
    ordering = ['category']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
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
        else:
            return Product.objects.none()

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            name='ordering',
            in_=openapi.IN_QUERY,
            description='Select a field to order the results by.',
            type=openapi.TYPE_STRING,
            enum=ordering_fields,
            required=False,
            example='category'
        ),
    ])
    def list(self, request, *args, **kwargs):
        # Votre logique de récupération de liste
        return super().list(request, *args, **kwargs)


class FriendListViewset(ModelViewSet):
    serializer_class = FriendListSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'delete']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return FriendList.objects.filter(user=user)
        else:
            return FriendList.objects.none()


class FriendRequestViewset(ModelViewSet):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return FriendRequest.objects.filter(Q(sender=user) | Q(receiver=user))
        else:
            return FriendRequest.objects.none()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sender_id = serializer.validated_data['sender']
        receiver_id = serializer.validated_data['receiver']

        sender = User.objects.get(id=sender_id)
        receiver = User.objects.get(id=receiver_id)

        if sender == receiver:
            return Response({"detail": "You cannot send a friend request to yourself."},
                            status=status.HTTP_400_BAD_REQUEST)

        sender_friend_list = FriendList.objects.get(user=sender)
        if sender_friend_list.is_mutual_friend(receiver):
            return Response({"detail": "You are already friends with this user."},
                            status=status.HTTP_400_BAD_REQUEST)

        existing_request = FriendRequest.objects.filter(sender=sender, receiver=receiver).first()
        if existing_request:
            return Response({"detail": "A friend request to this user is already active."},
                            status=status.HTTP_400_BAD_REQUEST)

        friend_request = FriendRequest(sender=sender, receiver=receiver)
        friend_request.save()

        # Créez la notification pour le receveur
        Notification.objects.create(
            user=receiver,
            friend_request=friend_request,
            content=_("New friend request from '{sender}'").format(sender=sender.surname),
        )

        return Response({"detail": "Friend request sent successfully."}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.sender != request.user and instance.receiver != request.user:
            return Response({"detail": "You do not have permission to delete this friend request."},
                            status=status.HTTP_403_FORBIDDEN)

        instance.delete()

        return Response({"detail": "Friend request deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        friend_request = self.get_object()

        if friend_request.receiver != request.user:
            return Response({"detail": "You do not have permission to accept this friend request."},
                            status=status.HTTP_403_FORBIDDEN)

        friend_request.accept()

        # Créez la notification pour le user qui a envoyé la demande d'ami
        Notification.objects.create(
            user=friend_request.sender,
            content=_("{receiver} accepted your friend request").format(receiver=friend_request.receiver.surname),
        )

        return Response({"detail": "Friend request accepted successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def decline(self, request, pk=None):
        friend_request = self.get_object()

        if friend_request.receiver != request.user:
            return Response({"detail": "You do not have permission to decline this friend request."},
                            status=status.HTTP_403_FORBIDDEN)

        friend_request.decline()

        # Créez la notification pour le user qui a envoyé la demande d'ami
        Notification.objects.create(
            user=friend_request.sender,
            content=_("{receiver} declined your friend request").format(receiver=friend_request.receiver.surname),
        )

        return Response({"detail": "Friend request declined successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        friend_request = self.get_object()

        if friend_request.sender != request.user:
            return Response({"detail": "You do not have permission to cancel this friend request."},
                            status=status.HTTP_403_FORBIDDEN)

        friend_request.cancel()

        return Response({"detail": "Friend request canceled successfully."}, status=status.HTTP_200_OK)


"""
NOTIFICATION VIEWSET
"""


class NotificationViewset(ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'delete']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Notification.objects.filter(user=user.id)
        else:
            return Notification.objects.none()
