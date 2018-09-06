from django.shortcuts import render


from django.views.generic.base import TemplateView


class LandingPage(TemplateView):
	template_name = 'website/landing.html'
