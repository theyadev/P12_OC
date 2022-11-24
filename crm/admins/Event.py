from django.contrib.admin import ModelAdmin


class EventAdmin(ModelAdmin):
    list_display = ('client', 'attendees', 'support_contact',
                    'date', 'created_at', 'updated_at')
    search_fields = ('date',  'client__first_name',
                     'client__last_name', 'support_contact__username')
    list_filter = ('support_contact', 'created_at', 'updated_at')
    ordering = ('date', 'created_at', 'updated_at', )
    filter_horizontal = ()
    list_per_page = 25
