from ..models import Contract, ContractStatus

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

    def save_model(self, request, obj, form, change):
        obj.sales_contact = request.user
        obj.save()

    def save_formset(self, request, form, formset, change):
        if formset.model == Contract:
            instances = formset.save(commit=False)
            for instance in instances:
                instance.sales_contact = request.user
                instance.save()
        else:
            formset.save()

    def has_delete_permission(self, request, obj=None):
        if not request.user.has_perm('auth.edit_own_contract'):
            return super().has_delete_permission(request, obj)

        if obj is None:
            return False

        return obj.client.sales_contact == request.user

    def has_change_permission(self, request, obj=None):
        if not request.user.has_perm('auth.edit_own_contract'):
            return super().has_change_permission(request, obj)

        if obj is None:
            return False

        return obj.client.sales_contact == request.user
