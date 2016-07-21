from viewflow import flow
from viewflow.base import Flow, this
from viewflow.flow.views import CreateProcessView
from .views import UpdateProcessView


from .nodes import PausableView
from .models import IncomingMailProcess


class IncomingMailFlow(Flow):
    process_cls = IncomingMailProcess

    start = (
        flow.Start(
            CreateProcessView,
            fields=['content'])
        .Next(this.gather_summary)
    )

    extract_summary = (
        PausableView(
            UpdateProcessView,
            fields=['summary', 'emergency', 'recipient'],
        )
        .Next(this.review)
    )

    review = (
        flow.View(
            UpdateProcessView,
            fields=['approved']
        )
        .Next(this.check_review)
    )

    check_review = (
        flow.If(lambda act: act.process.approved)
        .Then(this.end)
        .Else(this.gather_summary)
    )

    end = flow.End()
