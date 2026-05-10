from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin

class ActiveUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated:
            cache.set(f'seen_{request.user.username}', True, 300)
        return None
