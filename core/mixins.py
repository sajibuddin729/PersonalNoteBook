"""
Custom mixins for views and models
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

class UserOwnershipMixin(LoginRequiredMixin):
    """
    Mixin to ensure users can only access their own objects
    """
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

class NoteOwnershipMixin(LoginRequiredMixin):
    """
    Mixin specifically for note ownership
    """
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user and not obj.shared_users.filter(id=self.request.user.id).exists():
            raise PermissionDenied("You don't have permission to access this note.")
        return obj
