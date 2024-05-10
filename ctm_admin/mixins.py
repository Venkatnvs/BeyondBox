from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from django.http import HttpResponseForbidden

class CheckAdminMixin(LoginRequiredMixin,UserPassesTestMixin):
    model_permissions = None

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        elif self.model_permissions and self.request.user.user_type and self.request.user.is_staff:
            return all(
                all(
                    self.request.user.user_type.permissions.filter(
                        content_type__app_label=app_label,
                        codename=permission.lower()
                    ).exists()
                    for permission in permissions
                )
                for app_label, permissions in self.model_permissions.items()
            )
        return False

    def handle_no_permission(self):
        return HttpResponseForbidden("You don't have permission to access this page.")