from django.contrib.admin import ModelAdmin


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
