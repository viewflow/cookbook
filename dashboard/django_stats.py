import datetime
from dash import dcc, html
from django.db.models import Count
from django.db.models.functions import TruncDate, TruncMonth
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import User, Group
from django.utils import timezone
from viewflow.contrib.plotly import Dashboard, material


class DjangoStatsDashboard(Dashboard):
    app_name = 'django_stats'
    title = 'Django User Statistics'
    icon = 'public'

    def layout(self):
        return material.PageGrid([
            material.InnerRow([
                material.Span4([self.badge('Users registered', 'person', self.users_count())]),
                material.Span4([self.badge('Groups', 'group', self.groups_count())]),
                material.Span4([self.badge('Today admin actions', 'verified_user', self.users_count())]),
            ]),
            material.InnerRow([
                material.Span6([
                    dcc.Graph(figure=self.registration_stats_figure()),
                ]),
                material.Span6([
                    dcc.Graph(figure=self.login_stats_figure()),
                ])
            ]),
        ])

    def badge(self, title, icon, value):
        return html.Div([
            html.H6([
                html.I([icon], className="material-icons"),
                title,
            ], className="mdc-typography mdc-typography--headline6 vf-badge__header"),
            html.Span([value], className="mdc-typography vf-badge__value"),
        ], className="mdc-card mdc-card--outlined vf-badge")

    def users_count(self):
        return User.objects.filter(is_active=True).count()

    def groups_count(self):
        return Group.objects.count()

    def today_admin_actions(self):
        return LogEntry.objects.filter(
            action_time__gte=timezone.now().date()
        ).count()

    def login_stats_figure(self):
        today = timezone.now().date()
        data = {
            today + datetime.timedelta(days=day): 0
            for day in range(-5, 0)
        }

        logins_per_day = User.objects.filter(
            last_login__gte=today - timezone.timedelta(days=5),
        ).annotate(
            day=TruncDate('last_login')
        ).values(
            'day'
        ).annotate(
            cnt=Count('id')
        ).order_by(
            'day'
        ).values_list('day', 'cnt')

        for item in logins_per_day:
            data[item[0]] = item[1]

        return {
            'data': [{
                'type': 'bar',
                'x': list(data.keys()),
                'y': list(data.values()),
            }],
            'layout': {
                'title': 'Authenticated users',
                'plot_bgcolor': '#F9F9F9',
                'paper_bgcolor': '#F9F9F9',
                'xaxis': {
                    'tickformat': '%Y-%m-%d',
                    'nticks': len(data) + 1
                },
                'yaxis': {
                    'dtick': 1,
                }
            }
        }

    def registration_stats_figure(self):
        stats = User.objects.annotate(
            label=TruncMonth('date_joined')
        ).values('label').annotate(count=Count('id'))

        return {
            'data': [{
                'type': 'bar',
                'x': [item['label'] for item in stats],
                'y': [item['count'] for item in stats],

            }],
            'layout': {
                'title': 'Registration statistics',
                'plot_bgcolor': '#F9F9F9',
                'paper_bgcolor': '#F9F9F9',
                'xaxis': {
                    'tickformat': '%Y-%m-%d',
                },
                'yaxis': {
                    'dtick': 1,
                }
            }
        }
