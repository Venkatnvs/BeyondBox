from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test

def check_basic_auth(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            if request.user.is_authenticated and request.user.is_socialaccount and not request.user.is_completed:
                return redirect("accounts-complete-social")
        return view_func(request, *args, **kwargs)

    return _wrapped_view