from django.urls import path
from apps.system.api_views import (
    ProjectList,
    ProjectDetail,
    ProjectAppList,
    ProjectAppDetail,
    SystemList,
    SystemDetail,
    SystemModeratorList,
    SystemModeratorDetail,
    SystemDependencyList,
    SystemDependencyDetail,
    SystemAppList,
    SystemAppDetail,
)


urlpatterns = [
    path('', ProjectList.as_view()),
    path('<int:pk>/', ProjectDetail.as_view()),
    path('<int:project_id>/apps/', ProjectAppList.as_view()),
    path('<int:project_id>/apps/<int:pk>/', ProjectAppDetail.as_view()),

    path('<int:project_id>/systems/', SystemList.as_view()),
    path('<int:project_id>/systems/<int:pk>/', SystemDetail.as_view()),

    path(
        '<int:project_id>/systems/<int:pk>/dependencies/',
        SystemDependencyList.as_view()),
    path(
        '<int:project_id>/systems/<int:system_id>/dependencies/<int:pk>/',
        SystemDependencyDetail.as_view()),
    path(
        '<int:project_id>/systems/<int:system_id>/moderators/',
        SystemModeratorList.as_view()),
    path(
        '<int:project_id>/systems/<int:system_id>/moderators/<int:pk>/',
        SystemModeratorDetail.as_view()),
    path(
        '<int:project_id>/systems/<int:system_id>/apps/',
        SystemAppList.as_view()),
    path(
        '<int:project_id>/systems/<int:system_id>/apps/<int:pk>/',
        SystemAppDetail.as_view()),
]
