from rest_framework import permissions

class ISOwnerAdminForDeleteOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return True
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'DELETE':
            return obj.author == request.user or request.user.is_staff or request.user.is_superuser
        return True