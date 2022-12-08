from rest_framework.permissions import BasePermission


class IsSupportGroup(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Support').exists()
