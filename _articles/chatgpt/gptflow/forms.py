from django import forms

from viewflow.forms import ModelForm

from .models import Article, Summary


class ArticleSelectForm(ModelForm):
    article = forms.ModelChoiceField(
        queryset=Article.objects.all(),
        widget=forms.RadioSelect,
        required=True,
        label="Select an article for summary",
    )

    def __init__(self, *args, **kwargs):
        summary = kwargs.pop("summary", None)
        super().__init__(*args, **kwargs)

        if summary:
            self.fields["article"].queryset = Article.objects.filter(summary=summary)

    class Meta:
        model = Summary
        fields = ["article"]
