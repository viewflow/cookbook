from viewflow import this
from viewflow.workflow import flow, Activation
from viewflow.workflow.flow.views import CreateArtifactView, UpdateArtifactView
from viewflow.contrib import celery
from viewflow.forms import Layout, Row, FieldSet
from . import models, tasks
from .views import CreateArticleView, SelectArticleView


class NSplitActivation(flow.Split.activation_class):
    @Activation.status.super()
    def activate(self):
        for node, cond in self.flow_task._branches:
            if cond is None or cond(self):
                for _ in range(self.flow_task._count):
                    self.next_tasks.append(node)


class NSplit(flow.Split):
    activation_class = NSplitActivation

    def __init__(self, count, **kwargs):
        super().__init__(**kwargs)
        self._count = count


class VideoBriefFlow(flow.Flow):
    start = (
        flow.Start(
            CreateArtifactView.as_view(
                model=models.Summary,
                layout=Layout(
                    "url",
                    FieldSet(
                        "Request parameters",
                        Row("min_chapter_search", "max_chapter_search"),
                        Row("min_quote_search", "max_quote_search"),
                    ),
                    FieldSet("Template", "request_template"),
                ),
            )
        )
        .Permission(auto_create=True)
        .Next(this.fetch_video_data)
    )

    fetch_video_data = celery.Job(tasks.fetch_video_data_task).Next(
        this.edit_timestamps
    )

    edit_timestamps = (
        flow.View(
            UpdateArtifactView.as_view(
                model=models.Summary,
                fields=("video_timestamps",),
            )
        )
        .Permission(auto_create=True)
        .Next(this.load_subtitles)
    )

    load_subtitles = (
        flow.View(
            UpdateArtifactView.as_view(
                model=models.Summary,
                fields=("subtitles",),
            )
        )
        .Permission(auto_create=True)
        .Next(this.generate_chapters)
    )

    generate_chapters = celery.Job(tasks.generate_summary_task).Next(
        this.split_articles
    )

    split_articles = NSplit(3).Next(this.create_article_claude)

    create_article_claude = (
        flow.View(CreateArticleView.as_view())
        .Annotation(title="Create an article using Claude")
        .Permission(auto_create=True)
        .Next(this.join_articles)
    )

    join_articles = flow.Join().Next(this.select_article)

    select_article = (
        flow.View(SelectArticleView.as_view())
        .Permission(auto_create=True)
        .Next(this.end)
    )

    end = flow.End()

    create_article = flow.Obsolete()
    create_article_chatgpt = flow.Obsolete()
