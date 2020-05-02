from django.contrib import admin

# Register your models here.
from .models import Expertise
from .models import User
from .models import Project
from .models import Skill
from .models import Tag

admin.site.register(Expertise)
admin.site.register(User)
admin.site.register(Project)
admin.site.register(Skill)
admin.site.register(Tag)
