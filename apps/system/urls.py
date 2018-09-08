from django.urls import path
from apps.system.views import (
    ProjectPage,
    SystemPage,
)


urlpatterns = [
    path('/', ProjectPage.as_view()),
    path('<int:project_id>/', ProjectPage.as_view()),
    path('<int:project_id>/systems/<int:system_id>/', SystemPage.as_view()),
]
