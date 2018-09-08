
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import (
    ProjectModel,
    ProjectAppModel,
    SystemModel,
    SystemDependencyModel,
    SystemModeratorModel,
    SystemAppModel,
)


from .serializers import (
    ProjectSerializer,
    ProjectAppSerializer,
    SystemSerializer,
    SystemDependencySerializer,
    SystemModeratorSerializer,
    SystemAppSerializer,
)


class ProjectList(generics.ListCreateAPIView):
    queryset = ProjectModel.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, )


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProjectModel.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, )


class ProjectAppList(generics.ListCreateAPIView):
    queryset = ProjectAppModel.objects.all()
    serializer_class = ProjectAppSerializer
    permission_classes = (IsAuthenticated, )


class ProjectAppDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProjectAppModel.objects.all()
    serializer_class = ProjectAppSerializer
    permission_classes = (IsAuthenticated, )


class SystemList(generics.ListCreateAPIView):
    queryset = SystemModel.objects.all()
    serializer_class = SystemSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        return SystemModel.objects.filter(
            project_id=project_id).select_related('author')


class SystemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SystemModel.objects.all()
    serializer_class = SystemSerializer
    permission_classes = (IsAuthenticated, )


class SystemDependencyList(generics.ListCreateAPIView):
    queryset = SystemDependencyModel.objects.all()
    serializer_class = SystemDependencySerializer
    permission_classes = (IsAuthenticated, )


class SystemDependencyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SystemDependencyModel.objects.all()
    serializer_class = SystemDependencySerializer
    permission_classes = (IsAuthenticated, )


class SystemModeratorList(generics.ListCreateAPIView):
    queryset = SystemModeratorModel.objects.all()
    serializer_class = SystemModeratorSerializer
    permission_classes = (IsAuthenticated, )


class SystemModeratorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SystemModeratorModel.objects.all()
    serializer_class = SystemModeratorSerializer
    permission_classes = (IsAuthenticated, )


class SystemAppList(generics.ListCreateAPIView):
    queryset = SystemAppModel.objects.all()
    serializer_class = SystemAppSerializer
    permission_classes = (IsAuthenticated, )


class SystemAppDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SystemAppModel.objects.all()
    serializer_class = SystemAppSerializer
    permission_classes = (IsAuthenticated, )
