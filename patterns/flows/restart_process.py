from viewflow import this
from viewflow.workflow import flow


class RestartProcess(flow.Flow):
    """
    Description:
        Reuse data to start new process instance

    Examples:
        Allow user to send an application to review again

    Motivation:
        Looping in a business-prosses in most cases is an anypattern, makes
        thnis harderto manage and analyze. The more prominent way is to
        fail-fast, close old case and start new
    """
