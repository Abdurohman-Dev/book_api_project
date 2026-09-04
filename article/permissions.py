from rest_framework import permissions

class ISOwnerAdminForDeleteOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return True
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return obj.author == request.user or request.user.is_staff
        return True