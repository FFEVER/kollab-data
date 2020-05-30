from django.contrib import admin

from apps.api.models import RecAlgorithm, RecRequest, RecAlgorithmStatus, Endpoint


class EndpointAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')


class MLAlgorithmAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_endpoint', 'status', 'description', 'version', 'owner', 'created_at')

    def status(self, obj):
        return RecAlgorithmStatus.objects.filter(parent_mlalgorithm=obj).last().status


class MLAlgorithmStatusAdmin(admin.ModelAdmin):
    list_display = ('parent', 'status', 'active', 'endpoint', 'version', 'created_by', 'created_at')

    def parent(self, obj):
        return obj.parent_mlalgorithm

    def endpoint(self, obj):
        return obj.parent_mlalgorithm.parent_endpoint

    def version(self, obj):
        return obj.parent_mlalgorithm.version

class MLRequestAdmin(admin.ModelAdmin):
    list_display = ('parent_mlalgorithm', 'endpoint', 'input_data', 'full_response', 'created_at')

    def endpoint(self, obj):
        return obj.parent_mlalgorithm.parent_endpoint


admin.site.register(RecRequest, MLRequestAdmin)
admin.site.register(RecAlgorithmStatus, MLAlgorithmStatusAdmin)
admin.site.register(RecAlgorithm, MLAlgorithmAdmin)
admin.site.register(Endpoint, EndpointAdmin)
