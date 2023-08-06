from django.core.cache import cache


class RateLimit:
    def __init__(self, period, request):
        self.request = request
        self.key = ""
        self.time_periods = {
            "S": 1,
            "M": 60,
            "H": 3600,
            "D": 86400
        }
        if type(period) == str:
            try:
                self.seconds = int(period[:-1]) * self.time_periods[period[-1]]
            except ValueError as e:
                raise ValueError("Period must be String")
        else:
            raise ValueError("Period must be String")

    def get_limit(self):
        return cache.get_or_set(
            self.key, 0, timeout=self.seconds
        )

    def increment_request_limit(self):
        cache.incr(self.key, delta=1)

    def check(self):
        if self.get_limit() >= self.limit:
            return {
                "message": "Request limit exceeded",
                "status": 429
            }

        self.increment_request_limit()


class UserRateLimit(RateLimit):
    """
        This is to limit the authorized user requests 
    """
    cache_format = 'rl:%(ident)s'
    def __init__(self, request, limit, period):
        super().__init__(period, request)
        self.key = self.get_cache_key()
        self.limit = limit

    def get_cache_key(self):
        """
            Update the key_prefix for cache to store for authorized users
        """
        self.key = self.cache_format % {
            'ident': self.get_ident()
        }

    def get_ident(self):
        """
        Identify the user by ID
        """
        return str(self.request.user.id)


class AnonRateLimit(RateLimit):
    """
        This is to limit the anonymous user requests 
    """
    cache_format = 'rl:%(ident)s'

    def __init__(self, request, limit, period):
        super().__init__(period, request)
        self.key = self.get_cache_key()
        self.limit = limit

    def get_cache_key(self):
        """
            Update the key_prefix for cache to store for anonymous users
        """
        self.key = self.cache_format % {
            'ident': self.get_ident()
        }

    def get_ident(self):
        """
        Identify the machine making the request by parsing HTTP_X_FORWARDED_FOR
        if present. If not use all of
        HTTP_X_FORWARDED_FOR if it is available, if not use REMOTE_ADDR.
        """
        xff = self.request.META.get('HTTP_X_FORWARDED_FOR')
        remote_addr = self.request.META.get('REMOTE_ADDR')
        return ''.join(xff.split()) if xff else remote_addr
