from django import forms
from .models import Review


class ReviewCommentForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            "comment",
        ]
