from django.contrib import admin
from django.urls import path
from viewflow.urls import Site, Application
from viewflow.workflow.flow import FlowViewset
from cookbook.patterns.flows.sequence import Sequence
from cookbook.patterns.flows.exclusive_choice import ExclusiveChoice
from cookbook.patterns.flows.parallel_split_join import ParallelSplit
from cookbook.patterns.flows.deffered_choice import DefferedChoice
from cookbook.patterns.flows.multi_merge import MultiMerge
from cookbook.patterns.flows.partial_join import PartialJoin
from cookbook.patterns.flows.cancelling_partial_join import (
    CancelingPartialJoin,
)
from cookbook.patterns.flows.multiple_instances import MultipleInstances
from cookbook.patterns.flows.loop import Loop
from cookbook.patterns.flows.restart_process import RestartProcess
from cookbook.patterns.flows.withdraw_task import WithdrawTask
from cookbook.patterns.flows.terminate_process import TerminateProcess


site = Site(
    title="Workflow patterns",
    viewsets=[
        Application(
            title="Control",
            app_name="control",
            viewsets=[
                FlowViewset(Sequence, icon="start", title="Sequence"),
                FlowViewset(
                    ExclusiveChoice, icon="highlight_off", title="Exclusive Choice"
                ),
                FlowViewset(
                    ParallelSplit, icon="add_circle_outline", title="Parallel Split"
                ),
                FlowViewset(DefferedChoice, icon="add_circle", title="Deffered Choice"),
                FlowViewset(MultiMerge, icon="burst_mode", title="Multi Merge"),
                FlowViewset(PartialJoin, icon="bookmark", title="Partial Join"),
                FlowViewset(
                    CancelingPartialJoin,
                    icon="bookmarks",
                    title="Canceling Partial Join",
                ),
                FlowViewset(
                    MultipleInstances, icon="burst_mode", title="Multiple Instances"
                ),
                FlowViewset(Loop, icon="repeat", title="Loop"),
            ],
        ),
        Application(
            title="Livecycle",
            app_name="livecycle",
            viewsets=[
                FlowViewset(WithdrawTask, icon="u_turn_left", title="Withdraw Task"),
                # TODO Pause task?
                FlowViewset(
                    RestartProcess, icon="roundabout_left", title="Restart Process"
                ),
                FlowViewset(
                    TerminateProcess, icon="do_disturb_on", title="Terminate Process"
                ),
            ],
        ),
        Application(title="Resources", app_name="resources", viewsets=[]),
        Application(title="Data", app_name="data", viewsets=[]),
    ],
)

urlpatterns = [
    path("", site.urls),
    path("admin/", admin.site.urls),
]
