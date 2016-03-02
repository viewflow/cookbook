from django.conf.urls import patterns, url
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from customization.users.models import User


def users(request):
    return {
        'users': User.objects.order_by('-email')
    }


def login_as(request):
    user = request.REQUEST.get('user_pk', None)
    if user:
        try:
            user = User.objects.get(pk=user)
        except User.DoesNotExist:
            pass

    if user:
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
    else:
        logout(request)

    return redirect('/')


urlpatterns = patterns('',  # NOQA
    url(r'^login_as/$', login_as, name="login_as"))
