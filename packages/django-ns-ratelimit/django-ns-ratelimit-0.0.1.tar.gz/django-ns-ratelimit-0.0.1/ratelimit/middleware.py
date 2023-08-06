from django.http import JsonResponse
from ratelimit import UserRateLimit, AnonRateLimit



class UserRateLimitMiddleware:
    """
        This is used for authorized users rate limit request
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        user_ratelimit = UserRateLimit(request, 500, "1M").check()
        if user_ratelimit:
            return JsonResponse(user_ratelimit, status=429)
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response


class AnonRateLimitMiddleware:
    """
        This is used for anonymous users rate limit request
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        anon_ratelimit = AnonRateLimit(request, 500, "1M").check()
        if anon_ratelimit:
            return JsonResponse(anon_ratelimit, status=429)
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
