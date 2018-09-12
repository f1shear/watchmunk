from django.urls import path
from apps.system.api_views import (
    AppList,
    AppDetail,
    ProjectList,
    ProjectDetail,
    ProjectAccessList,
    ProjectAccessDetail,
    ProjectAppList,
    ProjectAppDetail,
    ProjectAppPostList,
    ProjectAppPostDetail,
    SystemList,
    SystemDetail,
    SystemAccessList,
    SystemAccessDetail,
    SystemModeratorList,
    SystemModeratorDetail,
    SystemDependencyList,
    SystemDependencyDetail,
    SystemAppList,
    SystemAppDetail,
    SystemAppPostList,
    SystemAppPostDetail,
)


urlpatterns = [
    path('projects/', ProjectList.as_view()),
    path('projects/<int:pk>/', ProjectDetail.as_view()),
    path('projects/<int:project_id>/accesses/', ProjectAccessList.as_view()),
    path('projects/<int:project_id>/accesses/<int:pk>/',
         ProjectAccessDetail.as_view()),
    path('apps/', AppList.as_view()),
    path('apps/<int:pk>/', AppDetail.as_view()),
    path('projects/<int:project_id>/apps/', ProjectAppList.as_view()),
    path('projects/<int:project_id>/apps/<int:pk>/', ProjectAppDetail.as_view()),
    path('projects/<int:project_id>/apps/<int:project_app_id>/posts/',
         ProjectAppPostList.as_view()),
    path('projects/<int:project_id>/apps/<int:project_app_id>/posts/<int:pk>/',
         ProjectAppPostDetail.as_view()),

    path('projects/<int:project_id>/systems/', SystemList.as_view()),
    path('projects/<int:project_id>/systems/<int:pk>/', SystemDetail.as_view()),

    path(
        'projects/<int:project_id>/systems/<int:system_id>/dependencies/',
        SystemDependencyList.as_view()),
    path(
        'projects/<int:project_id>/systems/<int:system_id>/dependencies/<int:pk>/',
        SystemDependencyDetail.as_view()),
    path(
        'projects/<int:project_id>/systems/<int:system_id>/moderators/',
        SystemModeratorList.as_view()),
    path(
        'projects/<int:project_id>/systems/<int:system_id>/moderators/<int:pk>/',
        SystemModeratorDetail.as_view()),
    path(
        'projects/<int:project_id>/systems/<int:system_id>/accesses/',
        SystemAccessList.as_view()),
    path(
        'projects/<int:project_id>/systems/<int:system_id>/accesses/<int:pk>/',
        SystemAccessDetail.as_view()),
    path(
        'projects/<int:project_id>/systems/<int:system_id>/apps/',
        SystemAppList.as_view()),
    path(
        'projects/<int:project_id>/systems/<int:system_id>/apps/<int:pk>/',
        SystemAppDetail.as_view()),

    path(
        'projects/<int:project_id>/systems/<int:system_id>/apps/<int:system_app_id>/posts/',
        SystemAppPostList.as_view()),
    path(
        'projects/<int:project_id>/systems/<int:system_id>/apps/<int:system_app_id>/posts/<int:pk>/',
        SystemAppPostDetail.as_view()),
]
