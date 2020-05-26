from django.contrib import admin

from apps.kstorage.models import User
from apps.kstorage.models import Project


class UserAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'email', 'role', 'faculty_id', 'fields', 'skills', 'joined_projects', 'starred_projects', 'viewed_projects',
    'followed_projects')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'project_status', 'fields', 'tags', 'created_at', 'updated_at')


admin.site.register(User, UserAdmin)
admin.site.register(Project, ProjectAdmin)

