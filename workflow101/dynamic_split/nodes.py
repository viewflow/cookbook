from viewflow import this
from viewflow.workflow import Activation, FlowRuntimeError, Node, Token, flow
from viewflow.workflow.nodes import mixins
from viewflow.workflow.flow import views


class DynamicSplitActivation(Activation):
    def __init__(self, *args, **kwargs):  # noqa D102
        self.next_tasks = []
        super().__init__(*args, **kwargs)

    @Activation.status.super()
    def activate(self):
        split_count = self.flow_task._task_count_callback(self)
        if split_count:
            self.next_tasks = [self.flow_task._next for _ in range(split_count)]
        elif self.flow_task._if_none_next_node is not None:
            self.next_tasks = [self.flow_task._if_none_next_node]
        else:
            raise FlowRuntimeError("{} activated with zero and no IfNone nodes specified".format(self.flow_task.name))

    @Activation.status.super()
    def create_next(self):
        """Activate next tasks for parallel execution.

        Each task would have a new execution token attached,
        the Split task token as a common prefix.
        """
        token_source = Token.split_token_source(self.task.token, self.task.pk)

        for n, next_task in enumerate(self.next_tasks, 1):
            yield next_task._create(prev_activation=self, token=next(token_source))


class DynamicSplit(
    flow.NodeDetailMixin,
    flow.NodeExecuteMixin,
    mixins.NextNodeMixin,
    mixins.NodeUndoMixin,
    mixins.NodeCancelMixin,
    Node,
):
    """
    Activates several outgoing task instances depends on callback value

    Example::

        spit_on_decision = flow.DynamicSplit(lambda p: 4) \\
            .Next(this.make_decision)

        make_decision = flow.View(MyView) \\
            .Next(this.join_on_decision)

        join_on_decision = flow.Join() \\
            .Next(this.end)
    """
    task_type = 'PARALLEL_GATEWAY'

    shape = {
        "width": 50,
        "height": 50,
        "svg": """
            <path class="gateway" d="M25,0L50,25L25,50L0,25L25,0"/>
            <text class="gateway-marker" font-size="32px" x="25" y="35">+</text>
        """,
    }

    index_view_class = views.IndexTaskView
    detail_view_class = views.DetailTaskView
    # cancel_view_class = views.CancelTaskView
    # perform_view_class = views.PerformTaskView
    # undo_view_class = views.UndoTaskView

    activation_class = DynamicSplitActivation

    def __init__(self, callback):
        super(DynamicSplit, self).__init__()
        self._task_count_callback = callback
        self._if_none_next_node = None

    def _resolve(self, instance):
        super()._resolve(instance)
        self._if_none_next_node = this.resolve(instance, self._if_none_next_node)

    def IfNone(self, node):
        self._if_none_next_node = node
        return self
