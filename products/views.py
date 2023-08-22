from friends.models import Notification
from .models import Product, Category, Reservation
from .serializers import ProductSerializer, CategorySerializer, ReservationSerializer

from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from api.permissions import IsAdminAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils.translation import gettext as _

"""
ADMIN VIEWSET
"""


class AdminProductViewset(ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminAuthenticated]

    queryset = Product.objects.all()


class AdminReservationViewset(ModelViewSet):
    serializer_class = ReservationSerializer
    permission_class = [IsAuthenticated]

    queryset = Reservation.objects.all()


"""
CATEGORY VIEWSET
"""


class CategoryViewset(ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    queryset = Category.objects.all()


"""
PRODUCT AND RESERVATION VIEWSET
"""


class ProductViewset(ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Product.objects.filter(owner=user)
        else:
            return Product.objects.none()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ReservationViewset(ModelViewSet):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Reservation.objects.filter(Q(requester=user) | Q(product__owner=user))
        else:
            return Reservation.objects.none()

    def perform_create(self, serializer):
        serializer.save(requester=self.request.requester)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data['product'].id
        product = get_object_or_404(Product, id=product_id)

        if product.status != 'AVAILABLE':
            return Response({"detail": "The selected product is not available for reservation."},
                            status=status.HTTP_400_BAD_REQUEST)

        reservation = Reservation(product=product, requester=self.request.user)
        reservation.save()

        product.status = 'BOOKED'
        product.save()

        Notification.objects.create(
            user=product.owner,
            reservation=reservation,
            content=_("New reservation from '{requester}' for '{product}'").format(
                requester=self.request.user.surname, product=product.name),
        )

        return Response({"detail": "Reservation sent successfully."}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        reservation_request = self.get_object()
        product = reservation_request.product

        if reservation_request.status != 'PENDING':
            return Response({'message': 'Reservation request is not pending'}, status=status.HTTP_400_BAD_REQUEST)

        if product.status != 'BOOKED':
            return Response({'message': 'Product is not booked for reservation'}, status=status.HTTP_400_BAD_REQUEST)

            # Mettre à jour le statut de la réservation
        reservation_request.status = 'ACCEPTED'
        reservation_request.save()

        # Mettre à jour le statut du produit
        product.status = 'BORROWED'
        product.save()

        # Créer une notification pour le demandeur de réservation
        Notification.objects.create(
            user=reservation_request.requester,
            content=_("Your reservation request for '{product}' has been accepted.").format(product=product.name),
        )

        return Response({'message': 'Reservation request accepted'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def decline(self, request, pk=None):
        reservation_request = self.get_object()
        product = reservation_request.product

        if reservation_request.status != 'PENDING':
            return Response({'message': 'Reservation request is not pending'}, status=status.HTTP_400_BAD_REQUEST)

        if product.status != 'BOOKED':
            return Response({'message': 'Product is not booked for reservation'}, status=status.HTTP_400_BAD_REQUEST)

        # Mettre à jour le statut de la réservation
        reservation_request.status = 'DECLINED'
        reservation_request.save()

        # Mettre à jour le statut du produit
        product.status = 'AVAILABLE'
        product.save()

        # Créer une notification pour le demandeur de réservation
        Notification.objects.create(
            user=reservation_request.requester,
            content=_("Your reservation request for '{product}' has been declined.").format(product=product.name),
        )

        return Response({'message': 'Reservation request declined'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        reservation_request = self.get_object()
        product = reservation_request.product

        if reservation_request.requester != request.user:
            return Response({"detail": "You do not have permission to cancel this reservation."},
                            status=status.HTTP_403_FORBIDDEN)

        # Supprimer la réservation
        reservation_request.delete()

        # Mettre à jour le statut du produit
        product.status = 'AVAILABLE'
        product.save()

        return Response({"detail": "Reservation canceled successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def return_product(self, request, pk=None):
        reservation = self.get_object()
        product = reservation.product

        if reservation.requester != request.user and product.owner != request.user:
            return Response({"detail": "You do not have permission to return this product."},
                            status=status.HTTP_403_FORBIDDEN)

        if product.status != 'BORROWED':
            return Response({'message': 'Product is not borrowed'}, status=status.HTTP_400_BAD_REQUEST)

        # Mettre à jour le statut de la réservation
        reservation.delete()

        # Mettre à jour le statut du produit
        product.status = 'AVAILABLE'
        product.save()

        return Response({"detail": "Product returned successfully."}, status=status.HTTP_200_OK)
