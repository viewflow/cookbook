from django.conf.urls import url, include


urlpatterns = [
    url(r'^', include('pause.incoming_mail.urls', namespace='incoming_mail')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='logout'),
]
