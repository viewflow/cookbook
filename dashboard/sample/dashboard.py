from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncDay
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.template.loader import render_to_string

import dashboard

User = get_user_model()


def users_count(request):
    return render_to_string('dashboard/counter.html', {
        'title': 'Users',
        'count': User.objects.count(),
        'icon': '<i class="material-icons">account_circle</i>'
    })


def groups_count(request):
    return render_to_string('dashboard/counter.html', {
        'title': 'Groups',
        'count': Group.objects.count(),
        'icon': '<i class="material-icons">perm_identity</i>'
    })


def staff_count(request):
    User = get_user_model()

    return render_to_string('dashboard/counter.html', {
        'title': 'Staff',
        'count': User.objects.filter(is_staff=True).count(),
        'icon': '<i class="material-icons">supervisor_account</i>'
    })


def registration_stats(request):
    stats = (
        User.objects
        .annotate(label=TruncMonth('date_joined'))
        .values('label')
        .annotate(count=Count('id'))
    )
    return render_to_string('dashboard/stats.html', {
        'title': 'User registration statistics',
        'stats': [
            {'label': user['label'].strftime('%Y-%m'),
             'count': user['count']}
            for user in stats
        ]
    })


def login_stats(request):
    stats = [
        {'label': user['label'].strftime('%Y-%m-%d'),
         'count': user['count']}
        for user in User.objects
        .filter(last_login__isnull=False)
        .annotate(label=TruncDay('last_login'))
        .values('label')
        .annotate(count=Count('id'))[:90]
    ]
    return render_to_string('dashboard/stats.html', {
        'title': 'User login statistics',
        'stats': stats
    })


dashboard.register('Welcome', [
    [users_count, groups_count, staff_count],
    [registration_stats, login_stats]
])


dashboard.register('Second', [
    [registration_stats, login_stats],
    [users_count, groups_count, staff_count]
])
