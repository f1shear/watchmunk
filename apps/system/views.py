from django.shortcuts import render

from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404

from apps.system.models import ProjectModel, SystemModel


class ProjectPage(TemplateView):
    template_name = 'system/project.html'


class SystemPage(TemplateView):
    template_name = 'system/system.html'
