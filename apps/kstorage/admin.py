from django.contrib import admin

from apps.kstorage.models import Expertise
from apps.kstorage.models import User
from apps.kstorage.models import Project
from apps.kstorage.models import Skill
from apps.kstorage.models import Tag

admin.site.register(Expertise)
admin.site.register(User)
admin.site.register(Project)
admin.site.register(Skill)
admin.site.register(Tag)
