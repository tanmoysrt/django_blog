from django.contrib.auth import logout
from django.shortcuts import redirect
from functools import wraps


def admin_required(view_func):
    @wraps(view_func)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.category != "normal":
            return view_func(request, *args, **kwargs)

        logout(request)
        return redirect('/login/')

    return wrap

def superadmin_required(view_func):
    @wraps(view_func)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.category == "superadmin":
            return view_func(request, *args, **kwargs)

        logout(request)
        return redirect('/login/')

    return wrap