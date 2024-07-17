from viewflow import this
from viewflow.workflow import flow


class WithdrawTask(flow.Flow):
    """
    Description
        An enabled task is withdrawn prior to it commencing execution. If the
        task has started, it is disabled and, where possible, the currently
        running instance is halted and removed.

    Examples
        The purchaser can cancel their building inspection task at any time
        before it commences.

    Motivation
        The Cancel Task pattern provides the ability to withdraw a task which
        has been enabled or is already executing. This ensures that it will not
        commence or complete execution.
    """

    # TODO flow.View().OnWithdraw(then=this.next_task_withdraw, permission='', view=this.withdraw_view)
