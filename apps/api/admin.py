from django.contrib import admin

from apps.api.models import RecAlgorithm, RecRequest, RecAlgorithmStatus, Endpoint


class EndpointAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')


class RecAlgorithmAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_endpoint', 'status', 'description', 'version', 'owner', 'created_at')

    def status(self, obj):
        return RecAlgorithmStatus.objects.filter(parent_mlalgorithm=obj).last().status


class RecAlgorithmStatusAdmin(admin.ModelAdmin):
    list_display = ('parent', 'status', 'active', 'endpoint', 'version', 'created_by', 'created_at')

    def parent(self, obj):
        return obj.parent_algorithm

    def endpoint(self, obj):
        return obj.parent_algorithm.parent_endpoint

    def version(self, obj):
        return obj.parent_algorithm.version

class RecRequestAdmin(admin.ModelAdmin):
    list_display = ('parent_algorithm', 'endpoint', 'input_data', 'full_response', 'created_at')

    def endpoint(self, obj):
        return obj.parent_algorithm.parent_endpoint


admin.site.register(RecRequest, RecRequestAdmin)
admin.site.register(RecAlgorithmStatus, RecAlgorithmStatusAdmin)
admin.site.register(RecAlgorithm, RecAlgorithmAdmin)
admin.site.register(Endpoint, EndpointAdmin)
