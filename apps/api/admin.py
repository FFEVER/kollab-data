from django.contrib import admin

# Register your models here.
from django.contrib import admin

from apps.api.models import MLAlgorithm, MLRequest, MLAlgorithmStatus, Endpoint

admin.site.register(MLRequest)
admin.site.register(MLAlgorithmStatus)
admin.site.register(MLAlgorithm)
admin.site.register(Endpoint)
