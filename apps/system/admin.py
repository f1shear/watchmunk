from django.contrib import admin

from .models import SystemModel, ProjectModel, ModeratorModel, DependencyModel


class ModeratorInline(admin.TabularInline):
    model = ModeratorModel


class DependencyInline(admin.TabularInline):
    model = DependencyModel
    fk_name = 'consumer'


@admin.register(SystemModel)
class SystemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'system_type', 'deployment_type', 'author', )
    inlines = [ModeratorInline, DependencyInline]


@admin.register(ProjectModel)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )
