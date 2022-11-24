from django.contrib.admin import ModelAdmin


class ContractStatusAdmin(ModelAdmin):
    list_display = ('name', 'created_at', )
    search_fields = ('name', )
    ordering = ('name', )
    filter_horizontal = ()
    list_per_page = 25
