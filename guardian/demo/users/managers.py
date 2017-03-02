from django.db import models
from django.contrib.auth.models import BaseUserManager


class DepartmentManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class UserManager(BaseUserManager):
    def get_by_natural_key(self, email):
        return self.get(email=email)

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        from . models import Department

        department, _ = Department.objects.get_or_create(
            name="Internal Control")

        return self.create_user(
            email=email,
            password=password,
            department=department,
            is_staff=True,
            is_superuser=True)
