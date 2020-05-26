from django.contrib import admin

from apps.ml.models import Relation


class RelationAdmin(admin.ModelAdmin):
    list_display = ('alg_type', 'row_type', 'col_type', 'row_count', 'col_count', 'created_at')

    list_filter = ('row_type', 'col_type', 'alg_type')


admin.site.register(Relation, RelationAdmin)
