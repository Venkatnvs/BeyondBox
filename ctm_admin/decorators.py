from functools import wraps,partial
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden

def check_admin(user, model_permissions):
    if user.is_superuser:
        return True
    elif model_permissions and user.user_type and user.is_staff:
        return all(
            all(
                user.user_type.permissions.filter(
                    content_type__app_label=app_label,
                    codename=permission.lower()
                ).exists()
                for permission in permissions
            )
            for app_label, permissions in model_permissions.items()
        )
    return False


def check_admin_required(view_func=None, model_permissions=None, login_url=None):
    if view_func is None:
        return partial(check_admin_required, model_permissions=model_permissions, login_url=login_url)

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts-login')
        if not check_admin(request.user, model_permissions):
            return HttpResponseForbidden("You don't have permission to access this page.")
        return view_func(request, *args, **kwargs)

    return wrapper
