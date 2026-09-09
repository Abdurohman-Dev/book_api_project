from rest_framework import permissions, request

class ISOwnerAdminForDeleteOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return True
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'DELETE':
            return obj.author == request.user or request.user.is_staff or request.user.is_superuser
        return True
class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.owner
class IsAdminOrOwnerStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner== request.user or request.is_staff or request.is_superuser
    