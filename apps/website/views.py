from django.shortcuts import render

from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404

from apps.system.models import ProjectModel, SystemModel


class LandingPage(TemplateView):
    template_name = 'website/landing.html'


class DashboardPage(TemplateView):
    template_name = 'website/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = ProjectModel.objects.all()
        return context


class ProjectPage(TemplateView):
    template_name = 'website/project.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = get_object_or_404(
            ProjectModel, id=self.kwargs.get('project_id'))
        context['systems'] = SystemModel.objects.filter(
            project_id=self.kwargs.get('project_id'))
        return context


class SystemPage(TemplateView):
    template_name = 'website/system.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['system'] = get_object_or_404(
            SystemModel, id=self.kwargs.get('system_id'))
        return context
