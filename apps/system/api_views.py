
from django.db.models import Q

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from rest_framework import exceptions


from .models import (
    AppModel,
    ProjectModel,
    ProjectAccessModel,
    ProjectAppModel,
    ProjectAppPostModel,
    SystemModel,
    SystemAccessModel,
    SystemDependencyModel,
    SystemAppModel,
    SystemAppPostModel,
)


from .serializers import (
    AppSerializer,
    ProjectSerializer,
    ProjectAccessSerializer,
    ProjectAppSerializer,
    ProjectAppPostSerializer,
    SystemSerializer,
    SystemAccessSerializer,
    SystemDependencySerializer,
    SystemAppSerializer,
    SystemAppPostSerializer,
)


from .permissions import (
    ProjectRelatedPermission,
    SystemRelatedPermission,
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

    def get_queryset(self):
        if self.request.user.is_superuser:
            qs = ProjectModel.objects.all()
        else:
            access_list = ProjectAccessModel.objects.filter(
                user=self.request.user).values_list('project_id', flat=True)
            access_list = list(access_list)
            qs = ProjectModel.objects.filter(
                Q(public=True) | Q(id__in=access_list))
        return qs

    def check_permissions(self, request):
        if self.request.method == 'GET':
            pass
        else:
            if not request.user.is_superuser:
                raise exceptions.PermissionDenied(
                    "Access Denied, Must be admin.")
        super(ProjectList, self).check_permissions(request)


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProjectModel.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, )

    def check_object_permissions(self, request, obj):
        can_read, can_write = False, False
        if obj.public:
            can_read = True
        if request.user.is_superuser:
            can_read, can_write = True, True
        else:
            try:
                project_access = ProjectAccessModel.objects.get(
                    user=request.user, project_id=obj.id)
            except ProjectAccessModel.DoesNotExist:
                project_access = None
            if project_access is not None:
                can_read, can_write = True, project_access.moderator
        if request.method == 'GET':
            if not can_read:
                raise exceptions.PermissionDenied("Access Denied")
        else:
            if not can_write:
                raise exceptions.PermissionDenied("Access Denied")
        super(ProjectDetail, self).check_object_permissions(request, obj)


class ProjectAccessList(generics.ListCreateAPIView):
    queryset = ProjectAccessModel.objects.all()
    serializer_class = ProjectAccessSerializer
    permission_classes = (
        IsAuthenticated, ProjectRelatedPermission)

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        return ProjectAccessModel.objects.filter(
            project_id=project_id).select_related('user')


class ProjectAccessDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProjectAccessModel.objects.all()
    serializer_class = ProjectAccessSerializer
    permission_classes = (IsAuthenticated, ProjectRelatedPermission)


class ProjectAppList(generics.ListCreateAPIView):

    serializer_class = ProjectAppSerializer
    permission_classes = (IsAuthenticated, ProjectRelatedPermission)

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        return ProjectAppModel.objects.filter(
            project_id=project_id)


class ProjectAppDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProjectAppModel.objects.all()
    serializer_class = ProjectAppSerializer
    permission_classes = (IsAuthenticated, ProjectRelatedPermission)


class ProjectAppPostList(generics.ListCreateAPIView):
    queryset = ProjectAppPostModel.objects.all()
    serializer_class = ProjectAppPostSerializer
    permission_classes = (IsAuthenticated, ProjectRelatedPermission)

    def get_queryset(self):
        project_app_id = self.kwargs.get('project_app_id')
        return ProjectAppPostModel.objects.filter(
            project_app_id=project_app_id)


class ProjectAppPostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProjectAppPostModel.objects.all()
    serializer_class = ProjectAppPostSerializer
    permission_classes = (IsAuthenticated, ProjectRelatedPermission)


class SystemList(generics.ListCreateAPIView):
    queryset = SystemModel.objects.all()
    serializer_class = SystemSerializer
    permission_classes = (IsAuthenticated, ProjectRelatedPermission)

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')

        if self.request.user.is_superuser:
            qs = SystemModel.objects.filter(
                project_id=project_id).select_related('author')
        else:

            try:
                project_access = ProjectAccessModel.objects.get(
                    user=self.request.user,
                    project_id=project_id)
            except ProjectAccessModel.DoesNotExist:
                project_access = None

            if project_access is not None and (
                    project_access.moderator or project_access.project.public):
                qs = SystemModel.objects.filter(project_id=project_id)
            else:
                allowed_list = SystemAccessModel.objects.filter(
                    user=self.request.user).values_list('system_id', flat=True)
                allowed_list = list(allowed_list)

                qs = SystemModel.objects.filter(
                    project_id=project_id).filter(
                    Q(public=True) |
                    Q(id__in=allowed_list)).select_related('author')
        return qs


class SystemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SystemModel.objects.all()
    serializer_class = SystemSerializer
    permission_classes = (IsAuthenticated, ProjectRelatedPermission)


class SystemAccessList(generics.ListCreateAPIView):
    queryset = SystemAccessModel.objects.all()
    serializer_class = SystemAccessSerializer
    permission_classes = (IsAuthenticated, SystemRelatedPermission)

    def get_queryset(self):
        system_id = self.kwargs.get('system_id')
        return SystemAccessModel.objects.filter(
            system_id=system_id).select_related('user')


class SystemAccessDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SystemAccessModel.objects.all()
    serializer_class = SystemAccessSerializer
    permission_classes = (IsAuthenticated, SystemRelatedPermission)


class SystemDependencyList(generics.ListCreateAPIView):

    serializer_class = SystemDependencySerializer
    permission_classes = (IsAuthenticated, SystemRelatedPermission)

    def get_queryset(self):
        system_id = self.kwargs.get('system_id')
        return SystemDependencyModel.objects.filter(
            system_id=system_id).select_related(
            'depends_on')


class SystemDependencyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SystemDependencyModel.objects.all()
    serializer_class = SystemDependencySerializer
    permission_classes = (IsAuthenticated, SystemRelatedPermission)


class SystemAppList(generics.ListCreateAPIView):
    serializer_class = SystemAppSerializer
    permission_classes = (IsAuthenticated, SystemRelatedPermission)

    def get_queryset(self):
        system_id = self.kwargs.get('system_id')
        return SystemAppModel.objects.filter(
            system_id=system_id).select_related(
            'app')


class SystemAppDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SystemAppModel.objects.all()
    serializer_class = SystemAppSerializer
    permission_classes = (IsAuthenticated, SystemRelatedPermission)


class SystemAppPostList(generics.ListCreateAPIView):
    serializer_class = SystemAppPostSerializer
    permission_classes = (IsAuthenticated, SystemRelatedPermission)

    def get_queryset(self):
        system_app_id = self.kwargs.get('system_app_id')
        return SystemAppPostModel.objects.filter(
            system_app_id=system_app_id)


class SystemAppPostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SystemAppPostModel.objects.all()
    serializer_class = SystemAppPostSerializer
    permission_classes = (IsAuthenticated, SystemRelatedPermission)
