from django.db import models

from viewflow import jsonstore

from .summary import ARTICLE_TASK_TEMPLATE, SUMMARY_TASK_TEMPLATE


class Article(models.Model):
    model = models.CharField(max_length=50)
    content = models.TextField()
    summary = models.ForeignKey("Summary", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.summary_id:
            return self.summary.title
        return super().__str__()


class Summary(models.Model):
    title = models.CharField(max_length=250, blank=True, null=True)
    url = models.URLField()
    subtitles = models.FileField(upload_to="subtitles/")
    video_timestamps = models.TextField(default="", blank=True)

    data = models.JSONField(default=dict)
    min_chapter_search = jsonstore.IntegerField(default=3)
    max_chapter_search = jsonstore.IntegerField(default=5)
    min_quote_search = jsonstore.IntegerField(default=3)
    max_quote_search = jsonstore.IntegerField(default=5)

    request_template = jsonstore.TextField(
        max_length=1024,
        default=SUMMARY_TASK_TEMPLATE,
    )

    chapters = models.TextField(default="", blank=True)
    result = models.ForeignKey(
        Article,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="+",
    )

    def __str__(self):
        return self.title or self.url

    @property
    def sections(self):
        return [
            line.strip() for line in self.video_timestamps.splitlines() if line.strip()
        ]

    def format_summary_request(self):
        return self.request_template.format(
            **{
                "min_chapter": self.min_chapter_search,
                "max_chapter": self.max_chapter_search,
                "min_quote": self.min_quote_search,
                "max_quote": self.max_quote_search,
            }
        )

    def format_article_request(self):
        return ARTICLE_TASK_TEMPLATE.format(
            title=self.title, chapters_count=max(int(len(self.sections) * 0.66), 12)
        )
