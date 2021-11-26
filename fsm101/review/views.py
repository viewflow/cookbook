from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import ReviewCommentForm
from .flows import ReviewFlow
from .models import Review


def reject_view(request, pk):
    review = get_object_or_404(Review, pk=pk)

    flow = ReviewFlow(
        review, user=request.user, ip_address=request.META.get("REMOTE_ADDR")
    )

    if not flow.reject.can_proceed() or not flow.reject.has_perm(request.user):
        raise PermissionDenied

    form = ReviewCommentForm(request.POST or None, instance=review)

    if request.method == "POST":
        form.save(commit=False)
        flow.reject()
        messages.add_message(
            request, messages.SUCCESS, "Review rejected", fail_silently=True
        )
        return redirect(reverse("review:list"))

    return render(request, "review/reject.html", {"form": form})
