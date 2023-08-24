from django.urls import path, include
from .views import (FriendListViewset, FriendRequestViewset, FriendListProductViewset, NotificationViewset,
                    AdminFriendListViewset, AdminFriendRequestViewset, AdminNotificationViewset)
from rest_framework import routers

router = routers.SimpleRouter()

router.register('friend_list', FriendListViewset, basename='friend-list')
router.register('friend_list/product', FriendListProductViewset, basename='friend-list-product')
router.register('friend_list/request', FriendRequestViewset, basename='friend-request')
router.register('notification', NotificationViewset, basename='notification')

router.register('admin/friend/list', AdminFriendListViewset, basename='admin-friend-list')
router.register('admin/friend/request', AdminFriendRequestViewset, basename='admin-friend-request')
router.register('admin/notification', AdminNotificationViewset, basename='admin-notification')

urlpatterns = [
    path('', include(router.urls)),
]
