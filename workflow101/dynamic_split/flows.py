from viewflow import this
from viewflow.workflow import flow, act
from viewflow.workflow.flow.views import CreateProcessView


from . import models, views
from .nodes import DynamicSplit


class DynamicSplitFlow(flow.Flow):
    """
    Dynamic split

    Depends on initial decision, several instances on make_decision task would be instantiated
    """

    process_class = models.DynamicSplitProcess

    process_title = "Dynamic split"
    process_description = "Custom Split node demo, with dynamic outgoing nodes count"
    process_goal_template = """
    Decision on: {{ process.question }}<br/>
    {{ process.decision_set.count }}  of {{ process.split_count }} completed
    """

    start = (
        flow.Start(CreateProcessView.as_view(fields=["question", "split_count"]))
        .Annotation(summary_template="Asks for {{ process.split_count }} decisions")
        .Permission(auto_create=True)
        .Next(this.spit_on_decision)
    )

    spit_on_decision = (
        DynamicSplit(act.process.split_count).Next(this.make_decision).IfNone(this.end)
    )

    make_decision = (
        flow.View(views.DecisionView.as_view())
        .Annotation(description="Decision required")
        .Next(this.join_on_decision)
    )

    join_on_decision = flow.Join().Next(this.end)

    end = flow.End()
