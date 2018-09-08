
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

from apps.user.serializers import UserSerializer


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectModel
        fields = '__all__'


class SystemSerializer(serializers.ModelSerializer):

    author = UserSerializer(read_only=True)

    class Meta:
        model = SystemModel
        fields = '__all__'

    def validate(self, data):
        if 'view' in self.context:
            project_id = self.context['view'].kwargs['project_id']
            try:
                data['project'] = ProjectModel.objects.get(id=project_id)
            except ProjectModel.DoesNotExist:
                raise serializers.ValidationError("Invalid Project")
        return data

    def create(self, validated_data):
        if 'request' in self.context:
            validated_data['author'] = self.context['request'].user
        return SystemModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key in validated_data:
            default = getattr(instance, key)
            setattr(
                instance, key, validated_data.get(key, default))
        return instance


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
