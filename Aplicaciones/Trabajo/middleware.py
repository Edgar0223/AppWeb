from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone

class UserActivityMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated and request.method == 'POST':
            request.user.capturando = True
            request.user.last_activity = timezone.now()
            request.user.save()

    def process_response(self, request, response):
        if request.user.is_authenticated and request.method != 'POST':
            request.user.capturando = False
            request.user.save()
        return response
