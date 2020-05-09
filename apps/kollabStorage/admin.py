from django.contrib import admin

from apps.kollabStorage.models import Expertise
from apps.kollabStorage.models import User
from apps.kollabStorage.models import Project
from apps.kollabStorage.models import Skill
from apps.kollabStorage.models import Tag

admin.site.register(Expertise)
admin.site.register(User)
admin.site.register(Project)
admin.site.register(Skill)
admin.site.register(Tag)
