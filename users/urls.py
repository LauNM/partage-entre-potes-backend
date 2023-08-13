from django.urls import path, include
from rest_framework import routers
from .views import UserViewset, AdminUserViewset


router = routers.SimpleRouter()

router.register('user', UserViewset, basename='user')

router.register('admin/user', AdminUserViewset, basename='admin-user')

urlpatterns = [
     path('api/', include(router.urls)),
]
