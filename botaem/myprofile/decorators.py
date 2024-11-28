from django.shortcuts import redirect


def require_post_redirect(redirect_url):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.method != 'POST':
                return redirect(redirect_url)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator