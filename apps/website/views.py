from django.shortcuts import render

from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404

from apps.system.models import ProjectModel, SystemModel


class LandingPage(TemplateView):
    template_name = 'website/landing.html'


class DashboardPage(TemplateView):
    template_name = 'website/dashboard.html'
