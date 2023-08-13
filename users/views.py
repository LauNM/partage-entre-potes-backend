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


"""
USER VIEWSET
"""


class UserViewset(ModelViewSet):
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
