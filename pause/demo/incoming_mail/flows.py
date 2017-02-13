from viewflow import flow, frontend
from viewflow.base import Flow, this
from viewflow.flow.views import CreateProcessView

from demo.nodes import PausableView
from demo.views import UpdateProcessView

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

frontend.register(IncomingMailFlow, FlowViewSet)