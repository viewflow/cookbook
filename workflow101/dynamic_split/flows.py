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
        DynamicSplit(act.process.split_count)
        .Next(this.make_decision)
        .IfNone(this.rejected)
    )

    make_decision = (
        flow.View(views.DecisionView.as_view())
        .Annotation(
            description="Decision required",
            result_template="{{ task.artifact.decision|yesno:'Approved,Rejected'}}",
        )
        .Next(this.join_on_decision)
    )

    join_on_decision = flow.Join(continue_on_condition=this.check_voting_complete).Next(
        this.check_result
    )

    check_result = flow.If(this.is_approved).Then(this.approved).Else(this.rejected)

    approved = flow.End()

    rejected = flow.End()

    def is_approved(self, activation):
        """
        Determines if the voting process is complete by approvement
        """
        true_count = activation.process.decision_set.filter(decision=True).count()
        return true_count > activation.process.split_count / 2

    def check_voting_complete(self, activation, _):
        """
        Determines if the voting process is complete by checking if the
        remaining unmade decisions would be unable to change the overall outcome
        of the vote.
        """
        answers = activation.process.decision_set.all()
        answers_count = len(answers)
        true_count = sum(answer.decision for answer in answers)

        min_additional_votes = abs(true_count - (answers_count - true_count)) + 1
        remaining_votes = activation.process.split_count - answers_count
        return remaining_votes < min_additional_votes
