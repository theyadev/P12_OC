from rest_framework.permissions import BasePermission


class IsSalesGroup(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Sales').exists()
