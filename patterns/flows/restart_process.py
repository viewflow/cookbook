"""
Description
    The passing of data elements from one case of a process during its execution to another case that is executing concurrently.

Example
    During execution of a case of the Re-balance Portfolio workflow the best price identified for each security is passed to other cases currently executing.

Motivation
   Where the results obtained during the course of one process instance are likely to be of use to other cases, a means of communicating them to both currently executing and subsequent cases is required.

"""
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

## https://stackoverflow.com/questions/61136760/allowing-users-to-select-which-flow-to-roll-back-to-django-viewflow
