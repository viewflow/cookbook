from django.conf import settings
from django.db import models
from django.contrib.auth import models as auth_models
from django.core.mail import send_mail
from guardian.mixins import GuardianUserMixin

from . import managers


class Department(models.Model):
    name = models.CharField(unique=True, max_length=250)
    description = models.TextField(blank=True)

    objects = managers.DepartmentManager()

    class Meta:
        permissions = (
            ('can_accept_bill', 'Can accept department bill'),
            ('can_sign_bill', 'Can sign department bill'),
            ('can_validate_bill', 'Can validate department bill'),
            ('can_set_bill_paydate', 'Can set payment date for department bill'),
            ('can_pay_bill', 'Can pay department bill'),
        )

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name, )


class User(GuardianUserMixin,
           auth_models.PermissionsMixin,
           auth_models.AbstractBaseUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    department = models.ForeignKey(Department, related_name='employees', on_delete=models.CASCADE)
    email = models.EmailField(unique=True, max_length=254)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = managers.UserManager()

    def natural_key(self):
        return (self.email,)

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])


def get_anonymous_user(self):
    department, _ = Department.objects.get_or_create(
        name="Internal Control")
    user, _ = User.objects.get_or_create(
        email=settings.ANONYMOUS_USER_NAME,
        department=department
    )
    return user
