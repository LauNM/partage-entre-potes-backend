from .models import Product, Category, Reservation
from .serializers import ProductSerializer, CategorySerializer, ReservationSerializer

from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from api.permissions import IsAdminAuthenticated
from rest_framework.decorators import action

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
        return Product.objects.filter(owner=user)


class ReservationViewset(ModelViewSet):
    serializer_class = ReservationSerializer
    permission_class = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def accept_request(self, request, pk=None):
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
            content=f"Your reservation request for '{product.name}' has been accepted.",
        )

        return Response({'message': 'Reservation request accepted'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def decline_request(self, request, pk=None):
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
            content=f"Your reservation request for '{product.name}' has been declined.",
        )

        return Response({'message': 'Reservation request declined'}, status=status.HTTP_200_OK)
