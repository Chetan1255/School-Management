from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def superadmin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        if request.user.role != "SUPER_ADMIN":
            return redirect('login')

        return view_func(request, *args, **kwargs)
    return wrapper