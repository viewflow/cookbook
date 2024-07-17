from viewflow import this
from viewflow.workflow import flow


class Trigger(flow.Flow):
    """
    Description:
        The ability for a task to be triggered by a signal from another part of
        the process or from the external environment. These triggers are
        persistent in form and are retained by the process until they can be
        acted on by the receiving task.

    Example:
        Initiate the Staff Induction task each time a new staff member event
        occurs

    Motivation
        Persistent triggers are inherently durable in nature, ensuring that they
        are not lost in transit and are buffered until they can be dealt with by
        the target task. This means that the singalling task can be certain that
        the trigger will result in the task to which the are directed being
        initiated either immediately (if it already has received the thread of
        control) or at some future time.

    """
