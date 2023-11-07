from rest_framework import status, generics, filters
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView


from django.contrib.auth.hashers import make_password
from .models import User
from products.models import Product
from friends.models import FriendList
from .serializers import (UserSerializer, UserListSerializer, RegisterSerializer, UserProfileSerializer,
                          UpdateUserProfileSerializer, UserSummarySerializer)
from api.permissions import IsAdminAuthenticated, IsOwnerOrReadOnly

"""
ADMIN VIEWSET
"""


class AdminUserViewset(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAdminAuthenticated]

    queryset = User.objects.all()

    def perform_create(self, serializer):
        # Hachage du mot de passe avant la création de l'utilisateur
        hashed_password = make_password(self.request.data['password'])
        serializer.save(password=hashed_password)


"""
USER VIEWSET
"""


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UserViewset(ModelViewSet):
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated & IsOwnerOrReadOnly]
    http_method_names = ['get']
    filter_backends = [filters.OrderingFilter]
    search_fields = ['surname']

    queryset = User.objects.all()


class UserListViewset(ModelViewSet):
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated & IsOwnerOrReadOnly]
    http_method_names = ['get']
    filter_backends = [filters.OrderingFilter]
    search_fields = ['surname']

    def get_queryset(self):
        user = self.request.user
        return User.objects.exclude(pk=user.id)


class UserProfileViewset(ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'delete']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return User.objects.filter(id=user.id)
        else:
            return User.objects.none()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance != request.user:
            return Response({"detail": "You do not have permission to delete this user."},
                            status=status.HTTP_403_FORBIDDEN)

        instance.delete()

        return Response({"detail": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class UpdateUserProfileViewset(ModelViewSet):
    serializer_class = UpdateUserProfileSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return User.objects.filter(id=user.id)
        else:
            return User.objects.none()

    def get_object(self):
        return self.request.user


class UserSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user

        # Calculez le nombre d'amis de l'utilisateur et la somme de leurs produits
        if hasattr(user, 'friends'):
            friends = FriendList.objects.get(user=user).friends.all()
            total_friends = friends.count()
            total_friends_products = Product.objects.filter(owner__in=friends).all().count()
        else:
            total_friends = 0
            total_friends_products = 0

        # Calculez le nombre de produits de l'utilisateur
        total_products = Product.objects.filter(owner=user).all().count()

        data = {
            'total_friends': total_friends,
            'total_products': total_products,
            'total_friends_products': total_friends_products
        }

        return Response(data)
