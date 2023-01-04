import logging

from rest_framework.permissions import BasePermission

logger = logging.getLogger(__name__)


class IsSupportGroup(BasePermission):
    def has_permission(self, request, view):
        res = request.user.groups.filter(name='Support').exists()

        if not res:
            logger.warning(f'User {request.user} is not in Support group')

        return res
