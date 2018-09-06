from django.shortcuts import render

from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404

from apps.system.models import ProjectModel, SystemModel


class ProjectPage(TemplateView):
    template_name = 'system/project.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = get_object_or_404(
            ProjectModel, id=self.kwargs.get('project_id'))
        context['systems'] = SystemModel.objects.filter(
            project_id=self.kwargs.get('project_id'))
        return context


class SystemPage(TemplateView):
    template_name = 'system/system.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['system'] = get_object_or_404(
            SystemModel, id=self.kwargs.get('system_id'))
        return context
