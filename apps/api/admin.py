from django.contrib import admin

from apps.api.models import RecAlgorithm, RecRequest, RecAlgorithmStatus, Endpoint
from django.utils.translation import ugettext_lazy as _


class EndpointAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')


class RecAlgorithmAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_endpoint', 'status', 'active', 'description', 'version', 'owner', 'created_at')

    list_filter = ('name', 'parent_endpoint', 'version')

    def status(self, obj):
        return RecAlgorithmStatus.objects.filter(parent_algorithm=obj).last().status

    def active(self, obj):
        return RecAlgorithmStatus.objects.filter(parent_algorithm=obj).last().active


class ParentAlgListFilter(admin.SimpleListFilter):
    title = _('Parent Algs')

    parameter_name = 'parent_algorithm'

    def lookups(self, request, model_admin):
        name_dict = RecAlgorithm.objects.values('name').distinct()
        return tuple([(name['name'], name['name']) for name in name_dict])

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        return queryset.filter(parent_algorithm__name=self.value())


class ParentEndpointFilter(admin.SimpleListFilter):
    title = _('Parent Endpoints')

    parameter_name = 'parent_endpoints'

    def lookups(self, request, model_admin):
        name_dict = RecAlgorithm.objects.values('parent_endpoint__name').distinct()
        return tuple([(name['parent_endpoint__name'], name['parent_endpoint__name']) for name in name_dict])

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        return queryset.filter(parent_algorithm__parent_endpoint__name=self.value())


def make_inactive(modeladmin, request, queryset):
    queryset.update(active=False)


def make_active(modeladmin, request, queryset):
    queryset.update(active=True)


def make_abtest(modeladmin, request, queryset):
    queryset.update(status="ab_testing")


def make_production(modeladmin, request, queryset):
    queryset.update(status="production")


make_active.short_description = "Mark as active"
make_inactive.short_description = "Mark as inactive"
make_abtest.short_description = "Mark as AB-Testing"
make_production.short_description = "Mark as production"


class RecAlgorithmStatusAdmin(admin.ModelAdmin):
    list_display = ('parent', 'status', 'active', 'endpoint', 'version', 'created_by', 'created_at')

    list_filter = (ParentEndpointFilter, ParentAlgListFilter, 'status', 'active',)

    actions = (make_inactive, make_active, make_abtest, make_production)

    def parent(self, obj):
        return obj.parent_algorithm

    def endpoint(self, obj):
        return obj.parent_algorithm.parent_endpoint

    def version(self, obj):
        return obj.parent_algorithm.version


class RecRequestAdmin(admin.ModelAdmin):
    list_display = ('parent_algorithm', 'endpoint', 'input_data', 'full_response', 'created_at')

    list_filter = ('parent_algorithm',)

    def endpoint(self, obj):
        return obj.parent_algorithm.parent_endpoint


admin.site.register(RecRequest, RecRequestAdmin)
admin.site.register(RecAlgorithmStatus, RecAlgorithmStatusAdmin)
admin.site.register(RecAlgorithm, RecAlgorithmAdmin)
admin.site.register(Endpoint, EndpointAdmin)
