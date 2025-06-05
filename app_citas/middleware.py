from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URLs que no requieren autenticación
        exempt_urls = [
            reverse('login'),
            reverse('registro'),
            '/admin/',
        ]

        if not request.user.is_authenticated and request.path not in exempt_urls and not request.path.startswith('/admin/'):
            return redirect('login')

        response = self.get_response(request)
        return response
