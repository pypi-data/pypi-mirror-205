# DJANGO-NS-RATELIMIT

## Project description
django-ns-ratelimit is django app for limit requests using rate limit class, decorators and middleware.

## Installation

```
pip install -i https://test.pypi.org/simple/ django-ns-ratelimit==1.0
```


## Usage

# Periods in format:
```
    S: For seconds
    M: For minutes
    H: For hour
    D: For Day

    e.g: "10S" "1M" "1D"
```

## Decorators
### user_method_ratelimit:
Used for user specific request rate limiting for class base apis

```
class SampleView(APIView):
    @user_method_ratelimit(5, "1M")
    def get(self, request):
        pass
```

### anon_method_ratelimit:
Used for Anonymous user requests rate limiting for class base apis

```
class SampleView(APIView):
    @anon_method_ratelimit(5, "1M")
    def get(self, request):
        pass
```

### user_func_ratelimit:
Used for user specific request rate limiting for function base apis

```
class SampleView(APIView):
    @user_func_ratelimit(5, "1M")
    def get(self, request):
        pass
```

### anon_func_ratelimit:
Used for Anonymous user requests rate limiting for function base apis

```
class SampleView(APIView):
    @anon_func_ratelimit(5, "1M")
    def get(self, request):
        pass
```

## Middlewares

### UserRateLimitMiddleware

Add this django settings Middlewares for User rate limiting
```
MIDDLEWARE = [
    .
    .
    .
    .
    "ratelimit.middleware.UserRateLimitMiddleware",
]
```

### AnonRateLimitMiddleware

Add this django settings Middlewares for Anonymous rate limiting
```
MIDDLEWARE = [
    .
    .
    .
    .
    "ratelimit.middleware.AnonRateLimitMiddleware",
]
```