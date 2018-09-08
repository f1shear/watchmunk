
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import (
    ProjectModel,
    SystemModel,
)


from .serializers import (
    ProjectSerializer,
    SystemSerializer,
)


class ProjectList(generics.ListCreateAPIView):
    queryset = ProjectModel.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, )


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProjectModel.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, )


class SystemList(generics.ListCreateAPIView):
    queryset = SystemModel.objects.all()
    serializer_class = SystemSerializer
    permission_classes = (IsAuthenticated, )


class SystemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SystemModel.objects.all()
    serializer_class = SystemSerializer
    permission_classes = (IsAuthenticated, )
