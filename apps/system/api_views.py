
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import (
    AppModel,
    ProjectModel,
    ProjectAppModel,
    ProjectAppPostModel,
    SystemModel,
    SystemDependencyModel,
    SystemModeratorModel,
    SystemAppModel,
    SystemAppPostModel,
)


from .serializers import (
    AppSerializer,
    ProjectSerializer,
    ProjectAppSerializer,
    ProjectAppPostSerializer,
    SystemSerializer,
    SystemDependencySerializer,
    SystemModeratorSerializer,
    SystemAppSerializer,
    SystemAppPostSerializer,
)


class AppList(generics.ListCreateAPIView):
    queryset = AppModel.objects.all()
    serializer_class = AppSerializer
    permission_classes = (IsAuthenticated, )


class AppDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AppModel.objects.all()
    serializer_class = AppSerializer
    permission_classes = (IsAuthenticated, )


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


class ProjectAppPostList(generics.ListCreateAPIView):
    queryset = ProjectAppPostModel.objects.all()
    serializer_class = ProjectAppPostSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        project_app_id = self.kwargs.get('project_app_id')
        return ProjectAppPostModel.objects.filter(
            project_app_id=project_app_id)


class ProjectAppPostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProjectAppPostModel.objects.all()
    serializer_class = ProjectAppPostSerializer
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

    serializer_class = SystemDependencySerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        system_id = self.kwargs.get('system_id')
        return SystemDependencyModel.objects.filter(
            system_id=system_id).select_related(
            'depends_on')


class SystemDependencyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SystemDependencyModel.objects.all()
    serializer_class = SystemDependencySerializer
    permission_classes = (IsAuthenticated, )


class SystemModeratorList(generics.ListCreateAPIView):
    queryset = SystemModeratorModel.objects.all()
    serializer_class = SystemModeratorSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        system_id = self.kwargs.get('system_id')
        return SystemModeratorModel.objects.filter(
            system_id=system_id).select_related(
            'moderator')


class SystemModeratorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SystemModeratorModel.objects.all()
    serializer_class = SystemModeratorSerializer
    permission_classes = (IsAuthenticated, )


class SystemAppList(generics.ListCreateAPIView):
    serializer_class = SystemAppSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        system_id = self.kwargs.get('system_id')
        return SystemAppModel.objects.filter(
            system_id=system_id).select_related(
            'app')


class SystemAppDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SystemAppModel.objects.all()
    serializer_class = SystemAppSerializer
    permission_classes = (IsAuthenticated, )


class SystemAppPostList(generics.ListCreateAPIView):
    serializer_class = SystemAppPostSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        system_app_id = self.kwargs.get('system_app_id')
        return SystemAppPostModel.objects.filter(
            system_app_id=system_app_id)


class SystemAppPostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SystemAppPostModel.objects.all()
    serializer_class = SystemAppPostSerializer
    permission_classes = (IsAuthenticated, )
