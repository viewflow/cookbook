from django.contrib import admin
from django.views import generic
from django.urls import path

from ..users import models


urlpatterns = [
    path('', generic.ListView.as_view(
        template_name='index.html',
        queryset=models.User.objects.select_subclasses(),
    )),
    path('employee/add/', generic.CreateView.as_view(
        template_name='form.html',
        model=models.Employee,
        fields=('username', 'hire_date', 'salary', 'department'),
        success_url='/',
    ), name='employee_add'),
    path('employee/<int:pk>/', generic.UpdateView.as_view(
        template_name='form.html',
        model=models.Employee,
        fields=('username', 'hire_date', 'salary', 'department'),
        success_url='/',
    ), name='employee_edit'),
    path('client/add/', generic.CreateView.as_view(
        template_name='form.html',
        model=models.Client,
        fields=('username', 'address', 'zip_code', 'city', 'vip'),
        success_url='/',
    ), name='client_add'),
    path('client/<int:pk>/', generic.UpdateView.as_view(
        template_name='form.html',
        model=models.Client,
        fields=('username', 'address', 'zip_code', 'city', 'vip'),
        success_url='/',
    ), name='client_edit'),
    path('admin/', admin.site.urls),
]
