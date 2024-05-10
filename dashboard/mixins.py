from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages

class CheckBasicAuthMixin(LoginRequiredMixin,UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_staff:
            return True
        if self.request.user.is_socialaccount:
            return self.request.user.is_completed
        return self.request.user.is_active

    def handle_no_permission(self):
        if not self.request.user:
            messages.warning(self.request, 'Complete your Account Setup')
            return redirect("accounts-complete-social")
        return super().handle_no_permission()