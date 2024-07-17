from viewflow import this
from viewflow.workflow import flow


class TerminateProcess(flow.Flow):
    """
    Description:
        A complete process instance is removed. This includes currently
        executing tasks, those which may execute at some future time and all
        sub-processes. The process instance is recorded as having completed
        unsuccessfully.

    Example:
        During a mortgage application, the purchaser decides not to continue
        with a house purchase and withdraws the application.

    Motivation
        This pattern provides a means of halting a specified process instance
        and withdrawing any tasks associated with it.
    """
