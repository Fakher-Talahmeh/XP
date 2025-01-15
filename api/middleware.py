
from django.utils.deprecation import MiddlewareMixin

class TokenFromSessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth_token = request.session.get('auth_token')
        if auth_token and not request.META.get('HTTP_AUTHORIZATION'):
            request.META['HTTP_AUTHORIZATION'] = f'Token {auth_token}'