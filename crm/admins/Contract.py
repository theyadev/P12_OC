from ..models.ContractStatus import ContractStatus
from django.contrib.admin import ModelAdmin, SimpleListFilter


class StatusFilter(SimpleListFilter):
    title = 'status'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [(status.id, status.name) for status in ContractStatus.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status__id=self.value())
        else:
            return queryset


class ContractAdmin(ModelAdmin):
    list_display = ('client', 'status',
                    'sales_contact', 'created_at', 'updated_at')
    list_filter = (StatusFilter,
                   'sales_contact', 'created_at', 'updated_at')
    search_fields = ('client__first_name', 'client__last_name', 'status__name', 'sales_contact__first_name',
                     'sales_contact__last_name', 'sales_contact__username')
    ordering = ('client', 'status',
                'sales_contact', 'created_at', 'updated_at')
    filter_horizontal = ()
    list_per_page = 25
