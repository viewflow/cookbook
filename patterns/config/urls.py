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
from cookbook.patterns.flows.service_tasks import ServiceTasks
from cookbook.patterns.flows.manual_task import ManualHandover
from cookbook.patterns.flows.timer_event import TimerDelay
from cookbook.patterns.flows.scheduled_start import ScheduledReport
from cookbook.patterns.flows.timer_boundary import ApprovalTimeout
from cookbook.patterns.flows.error_boundary import DeployRecovery
from cookbook.patterns.flows.terminate_end import RaceTerminate
from cookbook.patterns.flows.error_end import PaymentError
from cookbook.patterns.flows.subprocess import OrderFulfillment
from cookbook.patterns.flows.multi_instance import BatchReview
from cookbook.patterns.flows.compensation import BookingSaga


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
            title="Tasks",
            app_name="tasks",
            viewsets=[
                FlowViewset(
                    ServiceTasks, icon="mark_email_read", title="Service Tasks"
                ),
                FlowViewset(ManualHandover, icon="back_hand", title="Manual Task"),
            ],
        ),
        Application(
            title="Events",
            app_name="events",
            viewsets=[
                FlowViewset(TimerDelay, icon="timer", title="Timer Event"),
                FlowViewset(ScheduledReport, icon="schedule", title="Timer Start"),
                FlowViewset(ApprovalTimeout, icon="alarm", title="Timer Boundary"),
                FlowViewset(DeployRecovery, icon="error", title="Error Boundary"),
                FlowViewset(RaceTerminate, icon="cancel", title="Terminate End"),
                FlowViewset(PaymentError, icon="dangerous", title="Error End"),
            ],
        ),
        Application(
            title="Transactions",
            app_name="transactions",
            viewsets=[
                FlowViewset(OrderFulfillment, icon="account_tree", title="Subprocess"),
                FlowViewset(BatchReview, icon="dynamic_feed", title="Multi Instance"),
                FlowViewset(
                    BookingSaga, icon="settings_backup_restore", title="Compensation"
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
