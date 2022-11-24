from django.contrib.admin import ModelAdmin

from ..models.Client import Client


class ClientAdmin(ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'mobile',
                    'company_name', 'sales_contact', 'created_at', 'updated_at')
    list_filter = ('sales_contact', 'created_at', 'updated_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone',
                     'mobile', 'company_name', 'sales_contact__first_name', 'sales_contact__last_name', 'sales_contact__username')
    ordering = ('first_name', 'last_name', 'email', 'phone', 'mobile',
                'company_name', 'sales_contact', 'created_at', 'updated_at')
    filter_horizontal = ()
    list_per_page = 25

    def save_model(self, request, obj, form, change):
        obj.sales_contact = request.user
        obj.save()

    def save_formset(self, request, form, formset, change):
        if formset.model == Client:
            instances = formset.save(commit=False)
            for instance in instances:
                instance.sales_contact = request.user
                instance.save()
        else:
            formset.save()

    def has_view_permission(self, request, obj=None) -> bool:
        if not request.user.has_perm('auth.view_own_client'):
            return super().has_view_permission(request, obj)

        if obj is None:
            return True

        return obj.sales_contact == request.user

    def has_delete_permission(self, request, obj=None):
        if not request.user.has_perm('auth.edit_own_client'):
            return super().has_delete_permission(request, obj)

        if obj is None:
            return False

        return obj.sales_contact == request.user

    def has_change_permission(self, request, obj=None):
        if not request.user.has_perm('auth.edit_own_client'):
            return super().has_change_permission(request, obj)

        if obj is None:
            return False

        return obj.sales_contact == request.user
