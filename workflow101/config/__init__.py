from django.contrib.auth import login

from .celery import app as celery_app

__all__ = ('celery_app', 'AutoLoginMiddleware')


def AutoLoginMiddleware(get_response):
    def middleware(request):
        if request.user.is_anonymous:
            try:
                from django.contrib.auth.models import User
                user = User.objects.filter(is_superuser=True).first()
                if user:
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
            except User.DoesNotExist:
                pass

        response = get_response(request)
        return response

    return middleware
