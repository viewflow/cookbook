from openai import OpenAIError
from viewflow.contrib.celery import Job
from celery import shared_task, chord
from .models import Article
from .summary import (
    load_youtube_data,
    parse_srt,
    split_into_sections,
    get_section_summary,
    create_article,
)


@shared_task
def fetch_video_data_task(activation_ref):
    with Job.activate(activation_ref) as activation:
        summary = activation.process.artifact
        title, timestamps = load_youtube_data(summary.url)
        summary.title = title
        summary.video_timestamps = "\n".join(timestamps)
        summary.save()


@shared_task(
    autoretry_for=(OpenAIError,), retry_kwargs={"max_retries": 5}, retry_backoff=True
)
def generate_section_summary_task(pos, request, title, content):
    result = get_section_summary(request, {"title": title, "content": content})[0]
    return pos, title, result


@shared_task
def save_summary_task(results, activation_ref):
    with Job.activate(activation_ref, start=False, complete=True) as activation:
        summary = activation.process.artifact
        summary.chapters = "\n".join(
            f"Chapter: {title}\n\n{summary}" for _, title, summary in results
        )
        summary.save()


@shared_task
def generate_summary_task(activation_ref):
    with Job.activate(activation_ref, complete=False) as activation:
        summary = activation.process.artifact
        request = summary.format_summary_request()
        subtitles = parse_srt(summary.subtitles.path)
        splitted = split_into_sections(subtitles, summary.sections)

        subtasks = [
            generate_section_summary_task.s(
                n, request, section["title"], section["content"]
            )
            for n, section in enumerate(splitted)
        ]

        result = chord(subtasks)(save_summary_task.s(activation_ref))
        activation.task.data["chord_task_id"] = result.id


@shared_task(
    autoretry_for=(OpenAIError,), retry_kwargs={"max_retries": 5}, retry_backoff=True
)
def generate_article_task(activation_ref):
    with Job.activate(activation_ref) as activation:
        summary = activation.process.artifact
        request = summary.format_article_request()
        content = create_article(request, summary.chapters)
        activation.task.artifact = Article.objects.create(
            model="GPT3", content=content, summary=summary
        )
