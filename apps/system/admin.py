from django.contrib import admin

from .models import (
    SystemModel, ProjectModel, SystemDependencyModel,
    AppModel, ProjectAppModel, SystemAppModel,
    ProjectAccessModel, SystemAccessModel,
)


class ProjectAccessInline(admin.TabularInline):
    model = ProjectAccessModel


class SystemAccessInline(admin.TabularInline):
    model = SystemAccessModel


class SystemDependencyInline(admin.TabularInline):
    model = SystemDependencyModel
    fk_name = "system"


class ProjectAppInline(admin.TabularInline):
    model = ProjectAppModel


class SystemAppInline(admin.TabularInline):
    model = SystemAppModel


@admin.register(AppModel)
class AppAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )


@admin.register(SystemModel)
class SystemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'system_type', 'deployment_type', 'author', )
    inlines = [
        SystemAccessInline,
        SystemDependencyInline,
        SystemAppInline
    ]


@admin.register(ProjectModel)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )
    inlines = [ProjectAccessInline, ProjectAppInline, ]


@admin.register(ProjectAppModel)
class ProjectAppAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'app', )


@admin.register(SystemAppModel)
class SystemAppAdmin(admin.ModelAdmin):
    list_display = ('id', 'system', 'app', )
