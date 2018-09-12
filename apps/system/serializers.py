from rest_framework import serializers

from .models import (
    ProjectModel,
    ProjectAccessModel,
    SystemModel,
    SystemAccessModel,
    SystemModeratorModel,
    SystemDependencyModel,
    AppModel,
    ProjectAppModel,
    ProjectAppPostModel,
    SystemAppModel,
    SystemAppPostModel,
)

from apps.user.serializers import UserSerializer


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectModel
        fields = '__all__'


class ProjectAccessSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectAccessModel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProjectAccessSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            if self.context['request'].method == 'GET':
                self.fields['user'] = UserSerializer()


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
        instance.save()
        return instance


class SystemAccessSerializer(serializers.ModelSerializer):

    class Meta:
        model = SystemAccessModel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SystemAccessSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            if self.context['request'].method == 'GET':
                self.fields['user'] = UserSerializer()


class SystemModeratorSerializer(serializers.ModelSerializer):

    class Meta:
        model = SystemModeratorModel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SystemModeratorSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            if self.context['request'].method == 'GET':
                self.fields['moderator'] = UserSerializer()


class SystemDependencySerializer(serializers.ModelSerializer):

    class Meta:
        model = SystemDependencyModel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SystemDependencySerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            if self.context['request'].method == 'GET':
                self.fields['depends_on'] = SystemSerializer()


class AppSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppModel
        fields = '__all__'


class ProjectAppSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectAppModel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProjectAppSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            if self.context['request'].method == 'GET':
                self.fields['app'] = AppSerializer()


class SystemAppSerializer(serializers.ModelSerializer):

    class Meta:
        model = SystemAppModel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SystemAppSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            if self.context['request'].method == 'GET':
                self.fields['app'] = AppSerializer()


class ProjectAppPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectAppPostModel
        fields = '__all__'


class SystemAppPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = SystemAppPostModel
        fields = '__all__'
