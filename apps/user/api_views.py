
from rest_framework import generics

from .models import UserModel
from .serializers import UserSerializer


class UserList(generics.ListAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
