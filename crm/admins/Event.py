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

    def has_delete_permission(self, request, obj=None):
        if not request.user.has_perm('auth.edit_own_event'):
            return super().has_delete_permission(request, obj)

        if obj is None:
            return False

        return obj.supports_contact == request.user

    def has_change_permission(self, request, obj=None):
        if not request.user.has_perm('auth.edit_own_event'):
            return super().has_change_permission(request, obj)

        if obj is None:
            return False

        return obj.supports_contact == request.user

    def has_view_permission(self, request, obj=None) -> bool:
        return True
