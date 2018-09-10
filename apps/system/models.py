from django.db import models
from apps.user.models import UserModel


class ProjectModel(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField(default='', blank=True)

    class Meta:
        db_table = 'project'

    def __str__(self):
        return "%s" % self.name


class SystemModel(models.Model):
    SYSTEM_TYPES = (
        ('worker', 'Worker'),
        ('system', 'System'),
        ('storage', 'Storage'),
        ('queue', 'Queue'),
        ('database', 'Database'),
        ('web', 'Web'),
        ('client/web', 'Web Client'),
        ('client/desktop', 'Desktop Client'),
        ('client/mobile', 'Mobile Client'),
    )
    DEPLOYMENT_TYPES = (
        ('shared', 'Shared Hosting'),
        ('dedicated', 'Dedicated Server'),
        ('vm', 'Virtual Machine'),
        ('container', 'Container'),
        ('service', 'Service'),  # sqs
    )
    project = models.ForeignKey(
        'system.ProjectModel', related_name='project_systems',
        null=True, blank=True, on_delete=models.CASCADE)
    description = models.TextField(default='', blank=True)
    name = models.CharField(max_length=255)
    system_type = models.CharField(
        max_length=255, choices=SYSTEM_TYPES)
    repo_info = models.TextField(default='', blank=True)

    environment_config = models.TextField(default='', blank=True)
    staging_info = models.TextField(default='', blank=True)
    production_info = models.TextField(default='', blank=True)

    api_info = models.TextField(default='', blank=True)
    documentation = models.TextField(default='', blank=True)
    deployment_type = models.CharField(
        max_length=255, choices=DEPLOYMENT_TYPES)
    author = models.ForeignKey(
        UserModel, related_name='author_systems',
        null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'system'

    def __str__(self):
        return "%s" % self.name


class SystemModeratorModel(models.Model):
    system = models.ForeignKey(
        'system.SystemModel',
        related_name='moderators', on_delete=models.CASCADE)
    moderator = models.ForeignKey(
        'user.UserModel', related_name='+', on_delete=models.CASCADE)

    class Meta:
        db_table = 'system_moderator'
        unique_together = (('system', 'moderator'), )


class SystemDependencyModel(models.Model):
    system = models.ForeignKey(
        'system.SystemModel',
        related_name='dependencies', on_delete=models.CASCADE)
    depends_on = models.ForeignKey(
        'system.SystemModel',
        related_name='+', on_delete=models.CASCADE)

    class Meta:
        db_table = 'system_dependency'
        unique_together = (('system', 'depends_on'), )


class AppModel(models.Model):
    name = models.CharField(max_length=255)
    message_template = models.TextField(default='', blank=True)

    class Meta:
        db_table = 'app'

    def __str__(self):
        return self.name


class ProjectAppModel(models.Model):
    project = models.ForeignKey(
        'system.ProjectModel',
        related_name='project_apps', on_delete=models.CASCADE)
    app = models.ForeignKey(
        'system.AppModel', related_name='+', on_delete=models.CASCADE)

    class Meta:
        db_table = 'project_app'
        unique_together = (('project', 'app'), )

    def __str__(self):
        return "%s %s" % (self.project.name, self.app.name)


class ProjectAppPostModel(models.Model):

    project_app = models.ForeignKey(
        'system.ProjectAppModel', related_name='project_app_posts',
        on_delete=models.CASCADE)

    post = models.TextField()

    class Meta:
        db_table = 'project_app_post'


class SystemAppModel(models.Model):
    system = models.ForeignKey(
        'system.SystemModel',
        related_name='system_apps', on_delete=models.CASCADE)
    app = models.ForeignKey(
        'system.AppModel',
        related_name='+', on_delete=models.CASCADE)

    class Meta:
        db_table = 'system_app'
        unique_together = (('system', 'app'), )

    def __str__(self):
        return "%s %s" % (self.system.name, self.app.name)


class SystemAppPostModel(models.Model):

    system_app = models.ForeignKey(
        'system.SystemAppModel', related_name='system_app_posts',
        on_delete=models.CASCADE)

    post = models.TextField()

    class Meta:
        db_table = 'system_app_post'
