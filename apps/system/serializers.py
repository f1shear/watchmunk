
from rest_framework import serializers
from django.db import models

from .models import (
    ProjectModel,
    SystemModel,
    SystemModeratorModel,
    SystemDependencyModel,
    AppModel,
    ProjectAppModel,
    SystemAppModel,
)


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectModel
        fields = '__all__'


class SystemSerializer(serializers.ModelSerializer):

    class Meta:
        model = SystemModel
        fields = '__all__'


class SystemModeratorSerializer(serializers.ModelSerializer):

    class Meta:
        model = SystemModeratorModel
        fields = '__all__'


class SystemDependencySerializer(serializers.ModelSerializer):

    class Meta:
        model = SystemDependencyModel
        fields = '__all__'


class AppSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppModel
        fields = '__all__'


class ProjectAppSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectAppModel
        fields = '__all__'


class SystemAppSerializer(serializers.ModelSerializer):

    class Meta:
        model = SystemAppModel
        fields = '__all__'
