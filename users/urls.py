from django.urls import path, include
from rest_framework import routers
from .views import (UserViewset, UserListViewset, AdminUserViewset, RegisterView,
                    UserProfileViewset, UpdateUserProfileViewset, UserSummaryView)


router = routers.SimpleRouter()

router.register('user', UserViewset, basename='user')
router.register('user_list', UserListViewset, basename='user_list')
router.register('profile', UserProfileViewset, basename='profile')
router.register('profile/update', UpdateUserProfileViewset, basename='update_profile')


router.register('admin/user', AdminUserViewset, basename='admin-user')

urlpatterns = [
     path('register/', RegisterView.as_view(), name='auth_register'),
     path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
     path('profile/summary/', UserSummaryView.as_view(), name='user-summary'),
     path('', include(router.urls)),
]
