from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsHospitalAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user.hospital_admin


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_doctor


class IsVisitOwner(BasePermission):
    """
    Permission that allows to see visit details, only for client who booked this visit or
    only for doctor who own this visit
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            if obj.booking_visit.client.user == request.user:
                return True
        else:
            return obj.doctor == request.user.user_doctor


class IsBookingAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.visit.doctor.hospital == request.user.hospital_admin.hospital
