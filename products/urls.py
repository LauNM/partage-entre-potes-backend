from django.urls import path, include
from rest_framework import routers
from .views import (ProductViewset, CategoryViewset, ReservationViewset, AdminProductViewset, AdminReservationViewset)

router = routers.SimpleRouter()
router.register('product', ProductViewset, basename='product')
router.register('category', CategoryViewset, basename='category')
router.register('reservation', ReservationViewset, basename='reservation')

router.register('admin/product', AdminProductViewset, basename='admin-product')
router.register('admin/reservation', AdminReservationViewset, basename='admin-reservation')

urlpatterns = [
    path('', include(router.urls)),
]
