from django.contrib import admin

from .models import SystemModel, ProjectModel, ModeratorModel, DependencyModel

from .models import AppModel, ProjectAppModel, SystemAppModel


class ModeratorInline(admin.TabularInline):
    model = ModeratorModel


class DependencyInline(admin.TabularInline):
    model = DependencyModel
    fk_name = 'system'


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
    inlines = [ModeratorInline, DependencyInline, SystemAppInline]


@admin.register(ProjectModel)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )
    inlines = [ProjectAppInline, ]


@admin.register(ProjectAppModel)
class ProjectAppAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'app', )


@admin.register(SystemAppModel)
class SystemAppAdmin(admin.ModelAdmin):
    list_display = ('id', 'system', 'app', )
