from rest_framework import status, generics
from django.contrib.auth.hashers import make_password
from .models import User
from .serializers import (UserSerializer, UserListSerializer, RegisterSerializer, UserProfileSerializer,
                          UpdateUserProfileSerializer)
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from api.permissions import IsAdminAuthenticated, IsOwnerOrReadOnly
from rest_framework import filters
from rest_framework.response import Response

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


class UserProfileViewset(ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated & IsOwnerOrReadOnly]
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

