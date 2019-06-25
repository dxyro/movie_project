from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthenticatedOrReadOnlyCustom(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            if request.method.lower() == 'post':
                return request.user.is_authenticated

            return request.user.is_superuser
