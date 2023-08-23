from django.urls import path, include
from rest_framework import routers
from .views import UserViewset, AdminUserViewset, RegisterView, UserProfileViewset, UpdateUserProfileViewset


router = routers.SimpleRouter()

router.register('user', UserViewset, basename='user')
router.register('user/profile', UserProfileViewset, basename='profile')
router.register('user/profile/update', UpdateUserProfileViewset, basename='update_profile')


router.register('admin/user', AdminUserViewset, basename='admin-user')

urlpatterns = [
     path('register/', RegisterView.as_view(), name='auth_register'),
     path('', include(router.urls)),
]
