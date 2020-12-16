from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class ReviewState(models.IntegerChoices):
    NEW = 1, _('New')
    APPROVED = 2, _('Approved')
    REJECTED = 3, _('Rejected')
    PUBLISHED = 4, _('Published')
    HIDDEN = 5, _('Hidden')
    REMOVED = 6, _('Removed')

    def __str__(self):
        return str(self.value)


class Review(models.Model):
    stage = models.IntegerField(choices=ReviewState.choices)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    approver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        null=True, blank=True, related_name='+'
    )
    published = models.DateTimeField(null=True, blank=True)
    title = models.CharField(max_length=250)
    text = models.TextField()
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'#{self.pk} {self.title} by {self.author}'


class ReviewChangeLog(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE
    )
    changed = models.DateTimeField(default=timezone.now)
    source = models.IntegerField()
    target = models.IntegerField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    diff = models.TextField()
