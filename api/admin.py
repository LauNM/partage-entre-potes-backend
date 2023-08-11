from django.contrib import admin
from .models import Product, User, Category, FriendList, FriendRequest

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(FriendList)
admin.site.register(FriendRequest)

