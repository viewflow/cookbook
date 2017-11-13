from django.apps import apps
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect


def default_dashboard(request):
    '''Find first available dashboard'''
    module = apps.get_app_config('dashboard')

    for dashboard in module.dashboards():
        if dashboard.has_perm(request.user):
            return redirect('{}:dashboard'.format(module.label), dashboard.slug)

    raise PermissionDenied


def dashboard(request, slug):
    '''Find first available dashboard'''
    module = apps.get_app_config('dashboard')
    dashboard = module.get_dashboard(slug)
    if dashboard is None:
        raise Http404
    if not dashboard.has_perm(request.user):
        raise PermissionDenied

    return render(request, 'dashboard/index.html', {
        'dashboard': dashboard
    })
