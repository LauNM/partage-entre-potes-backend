from django.contrib import admin
from .models import Product, User, Category, FriendList, FriendRequest

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(User)


class FriendListAdmin(admin.ModelAdmin):
    list_filter = ['user']
    list_display = ['user']
    search_field = ['user']
    readonly_field = ['user']

    class Meta:
        model = FriendList


admin.site.register(FriendList, FriendListAdmin)


class FriendRequestAdmin(admin.ModelAdmin):
    list_filter = ['sender', 'receiver']
    list_display = ['sender', 'receiver']
    search_field = ['sender__username', 'receiver__username']

    class Meta:
        model = FriendRequest


admin.site.register(FriendRequest, FriendRequestAdmin)

