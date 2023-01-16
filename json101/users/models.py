from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.urls import reverse
from polymodels.managers import PolymorphicManager
from polymodels.models import PolymorphicModel
from viewflow import jsonstore


class UserManager(PolymorphicManager, UserManager):
    pass


class User(PolymorphicModel, AbstractUser):
    data = jsonstore.JSONField(null=True, default=dict)
    objects = UserManager()


class Employee(User):
    hire_date = jsonstore.DateField()
    salary = jsonstore.DecimalField(max_digits=10, decimal_places=2)
    department = jsonstore.CharField(max_length=200, choices=[
        ('Marketing', 'Marketing'),
        ('Development', 'Development'),
        ('Sales', 'Sales'),
    ])

    def get_absolute_url(self):
        return reverse('employee_edit', args=[self.pk])

    class Meta:
        proxy = True


class Client(User):
    address = jsonstore.CharField(max_length=250)
    zip_code = jsonstore.CharField(max_length=250)
    city = jsonstore.CharField(max_length=250)
    vip = jsonstore.BooleanField()

    def get_absolute_url(self):
        return reverse('client_edit', args=[self.pk])

    class Meta:
        proxy = True
