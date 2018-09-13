
from rest_framework import permissions
from .models import ProjectAccessModel, SystemAccessModel


class ProjectRelatedPermission(permissions.BasePermission):
    message = "Access Denied"

    def has_permission(self, request, view):
        """ global permission applies to list and detail view """
        if request.user.is_superuser:
            return True
        try:
            project_access = ProjectAccessModel.objects.get(
                project_id=view.kwargs.get('project_id'), user=request.user)
        except ProjectAccessModel.DoesNotExist:
            project_access = None

        if project_access is not None:
            if request.method in permissions.SAFE_METHODS:
                return True
            if project_access.moderator:
                return True

        return False


class SystemRelatedPermission(permissions.BasePermission):
    message = "Access Denied"

    def has_permission(self, request, view):
        """ global permission applies to list and detail view """
        if request.user.is_superuser:
            return True
        try:
            system_access = SystemAccessModel.objects.get(
                system_id=view.kwargs.get('system_id'), user=request.user)
            project = system_access.system.project
            project_access = ProjectAccessModel.objects.get(
                project=project, user=request.user)
            if project_access.moderator:
                return True
        except SystemAccessModel.DoesNotExist:
            system_access = None
        if system_access is not None:
            if request.method in permissions.SAFE_METHODS:
                return True
            if system_access.moderator:
                return True
        return False
