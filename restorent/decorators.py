from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages



def user_has_profile(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not hasattr(request.user, 'userprofile'):
            messages.error(request, 'user not allowed to show this page')
            return redirect('logout')