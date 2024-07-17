from viewflow import this
from viewflow.workflow import flow


class DutiesSeparation(flow.Flow):
    """
    Description
        The ability to specify that two tasks must be executed by different
        resources in a given case.

    Example
        Instances of the Countersign cheque task must be allocated to a differnt
        resource to that which executed the Prepare cheque task in a given case.

    Motivation
        Separation of Duties allows for the enforcement of audit controls within
        the execution of a given case. The Seperation of Duties constraint
        exists between two tasks in a process model. It ensures that within a
        given case, work items corresponding to the latter task cannot be
        executed by resources that completed work items corresponding to the
        former task. Another use of this pattern arises with PAIS that support
        multiple task instances. In this situation, the degree of parallelism
        that can be achieved when a multiple instance task is executed can be
        maximised by specifying that as far as possible no two task instances
        can be executed by the same resource.
    """
