from rest_framework.permissions import BasePermission


class IsFarmerOrExtensionOfficer(BasePermission):
    message = "You must be a farmer or extension officer to perform this action."

    def has_permission(self, request, view):
        return request.user.role in ["farmer", "extension_officer"]


class IsFarmerOrBuyer(BasePermission):
    message = "You must be a farmer or buyer to perform this action."

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ["farmer", "buyer"]


class IsFarmer(BasePermission):
    message = "You must be a farmer to perform this action."

    def has_permission(self, request, view):
        return request.user.role == "farmer"


class IsBuyer(BasePermission):
    message = "You must be a buyer to perform this action."

    def has_permission(self, request, view):
        return request.user.role == "buyer"


class IsExtensionOfficer(BasePermission):
    message = "You must be an extension officer to perform this action."

    def has_permission(self, request, view):
        return request.user.role == "extension_officer"


class IsOwnerOrReadOnly(BasePermission):
    message = "You must be the owner of this object to perform this action."

    def has_object_permission(self, request, view, obj):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        return obj.user == request.user


class ReadAccess(BasePermission):
    message = "You must be a farmer or extension officer to perform this action."

    def has_permission(self, request, view):
        # Allow read-only access for any authenticated user
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        # Allow write access only to farmers and extension officers
        return request.user.role in ["farmer", "extension_officer"]


class IsSenderOrReceiver(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user or obj.receiving_officer == request.user


class IsExtensionOfficerSender(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.responder == request.user
