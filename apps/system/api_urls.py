from django.urls import path
from apps.system.api_views import (
    ProjectList,
    ProjectDetail,
    SystemList,
    SystemDetail,
)


urlpatterns = [
    path('', ProjectList.as_view()),
    path('<int:pk>', ProjectDetail.as_view()),
    path('<int:project_id>/systems', SystemList.as_view()),
    path('<int:project_id>/systems/<int:pk>', SystemDetail.as_view()),
]
