from django.urls import path, include
from rest_framework import routers
from .views import (UserViewset, AdminUserViewset, RegisterView,
                    UserProfileViewset, UpdateUserProfileViewset)


router = routers.SimpleRouter()

router.register('user', UserViewset, basename='user')
router.register('profile', UserProfileViewset, basename='profile')
router.register('profile/update', UpdateUserProfileViewset, basename='update_profile')


router.register('admin/user', AdminUserViewset, basename='admin-user')

urlpatterns = [
     path('register/', RegisterView.as_view(), name='auth_register'),
     path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
     path('', include(router.urls)),
]
