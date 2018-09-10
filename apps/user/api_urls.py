from django.urls import path

from .api_views import UserList

urlpatterns = [
    path('', UserList.as_view()),
]
