from rest_framework import permissions


class CommentOwnerPermisson(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, comment):
        return request.user == comment.user


class BookingOwnerPermisson(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, booking):
        return request.user == booking.user