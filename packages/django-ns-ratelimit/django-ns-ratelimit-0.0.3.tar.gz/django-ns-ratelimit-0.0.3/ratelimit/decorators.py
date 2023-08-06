from functools import wraps
from django.http import JsonResponse
from ratelimit import UserRateLimit, AnonRateLimit


def user_method_ratelimit(limit, period):
    """
        This decorator is used for user rate limits and class based apis.
    """
    def internal(view_func):
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            user_ratelimit = UserRateLimit(request, limit, period).check()
            if user_ratelimit:
                return JsonResponse(user_ratelimit, status=429)
            return view_func(self, request, *args, **kwargs)

        return wrapper
    return internal


def anon_method_ratelimit(limit, period):
    """
        This decorator is used for anonymous rate limits and class based apis.
    """
    def internal(view_func):
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            anon_ratelimit = AnonRateLimit(request, limit, period).check()
            if anon_ratelimit:
                return JsonResponse(anon_ratelimit, status=429)
            return view_func(self, request, *args, **kwargs)

        return wrapper
    return internal


def user_func_ratelimit(limit, period):
    """
        This decorator is used for user rate limits and function based apis.
    """
    def internal(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user_ratelimit = UserRateLimit(request, limit, period).check()
            if user_ratelimit:
                return JsonResponse(user_ratelimit, status=429)

            return view_func(request, *args, **kwargs)

        return wrapper
    return internal


def anon_func_ratelimit(limit, period):
    """
        This decorator is used for anonymous rate limits and function based apis.
    """
    def internal(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            anon_ratelimit = AnonRateLimit(request, limit, period).check()
            if anon_ratelimit:
                return JsonResponse(anon_ratelimit, status=429)
            return view_func(request, *args, **kwargs)

        return wrapper
    return internal
