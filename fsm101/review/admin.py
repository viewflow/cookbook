from django.core.exceptions import PermissionDenied
from django.contrib import admin
from django.contrib.admin.utils import quote
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import path, reverse
from django.utils.translation import gettext_lazy as _
from reversion.admin import VersionAdmin
from viewflow import fsm

from .flows import ReviewFlow
from .forms import ReviewCommentForm
from .models import Review, ReviewChangeLog


@admin.register(Review)
class ReviewFlowAdmin(fsm.FlowAdminMixin, VersionAdmin):
    actions = None
    date_hierarchy = 'published'
    list_display = ('pk', 'author', 'published', 'approver', 'stage', )
    list_display_links = ('pk', 'author', )
    list_filter = ('stage', )
    fields = ('stage', 'author', 'approver', 'published', 'text', 'comment')
    readonly_fields = ('stage', 'author', 'approver', 'published', 'comment',)

    flow_state = ReviewFlow.stage

    def get_object_flow(self, request, obj):
        """Instantiate the flow without default constructor"""
        return ReviewFlow(
            obj, user=request.user,
            ip_address=request.META.get('REMOTE_ADDR')
        )

    def get_transition_fields(self, request, obj, slug):
        if slug == 'approve':
            return ['text', 'comment']

    def get_urls(self):
        """Custom transition view."""
        return [
            path('<path:object_id>/transition/reject/', self.admin_site.admin_view(self.reject_view),),
        ] + super().get_urls()

    def reject_view(self, request, object_id):
        """Custom transition view."""
        opts = self.model._meta
        obj = get_object_or_404(self.model, pk=object_id)
        form = ReviewCommentForm(request.POST or None, instance=obj)
        flow = self.get_object_flow(request, obj)
        if not flow.reject.has_perm(request.user) or not flow.reject.can_proceed():
            raise PermissionDenied

        if form.is_valid():
            form.save(commit=False)
            flow.reject()

            obj_url = reverse(
                'admin:%s_%s_change' % (opts.app_label, opts.model_name),
                args=(quote(obj.pk),),
                current_app=self.admin_site.name,
            )

            return HttpResponseRedirect(obj_url)

        return render(request, 'review/admin/approve.html', {
            'form': form,
            'opts': opts,
            'original': obj,
            'transition': flow.reject,
            'media': self.media,
            'title': _('Reject review'),
            'has_view_permission': self.has_view_permission(request, obj),
        })

    def save_model(self, request, obj, form, change):
        """Adding new objects are not handled by flow."""
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(ReviewChangeLog)
class ReviewChangeLogAdmin(admin.ModelAdmin):
    pass
