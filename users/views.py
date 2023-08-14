from django.contrib.auth.hashers import make_password
from .models import User
from .serializers import UserSerializer, UserListSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsAdminAuthenticated

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


class UserViewset(ModelViewSet):
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()

    def perform_create(self, serializer):
        # Hachage du mot de passe avant la création de l'utilisateur
        hashed_password = make_password(self.request.data['password'])
        serializer.save(password=hashed_password)
