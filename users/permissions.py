from rest_framework import permissions
# from rest_framework.exceptions import PermissionDenied

# ---------- USER RELATED PERMISSION ----------
# No any access permission
class NoAccessForAnonymous(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return True
    
class NoAccessForEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_employee:
            return False
        return True
# No any access permission
    
# Read only access permission
class ReadOnlyForAnonymous(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous and request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_anonymous and request.method not in permissions.SAFE_METHODS:
            return False
        return True
# Read only access permission

class NoCreateDeleteForEmployeeAndManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and not request.user.is_admin and (request.method == 'POST' or request.method == 'DELETE'):
            return False
        return True

class OwnDataUpdateOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if (request.user.is_authenticated and request.user.is_admin) or (request.method in permissions.SAFE_METHODS) or request.user == obj:
            return True
        return False
# ---------- USER RELATED PERMISSION ----------

# for claim category
class IsaAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method not in permissions.SAFE_METHODS and not request.user.is_admin:
            return False
        return True

# for claim request
class NoCreateAndDelPerm(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST' or request.method=='DELETE':
            return False
        return True
    
# report view and generate for admin only
class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated or not request.user.role == 'admin':
            return False
        return True