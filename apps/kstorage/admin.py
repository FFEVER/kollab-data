from django.contrib import admin

from apps.kstorage.models import User
from apps.kstorage.models import Project

admin.site.register(User)
admin.site.register(Project)
