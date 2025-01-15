"""
Description:
    Round Robin Allocation is a method of assigning tasks to a group of
    resources in a fair and equal way. Each task is given to a different
    resource in turn, cycling through all available resources.

Example:
    In a sports tournament, tasks for managing matches (like the "Umpire Match"
    task) are assigned to referees one by one in a cycle. If there are three
    referees, tasks are distributed as Referee 1 → Referee 2 → Referee 3 →
    Referee 1, and so on.

Purpose:
    Round Robin Allocation ensures tasks are distributed equally among
    resources. This method avoids overloading any single resource and promotes
    fairness in task allocation. It is particularly useful in scenarios where
    all resources have similar skills and responsibilities.
"""

from django.core.cache import cache
from django.db.models import Q
from django.contrib.auth.models import User
from django.test import TestCase
from viewflow import this, jsonstore
from viewflow.workflow import flow
from viewflow.workflow.flow.views import CreateProcessView, UpdateProcessView
from viewflow.workflow.models import Process


def get_next_referee(cache_key="round_robin_referee"):
    with cache.lock(f"{cache_key}_lock", timeout=2):  # global lock with django-redis
        referees = User.objects.filter(
            Q(groups__name__startswith="shipment/") | Q(groups__name="Referees")
        ).order_by("id")
        if not referees.exists():
            raise ValueError("No referees available")

        current_user_id = cache.get(cache_key)

        if current_user_id is None:
            next_referee = referees.first()
        else:
            next_referee = (
                referees.filter(id__gt=current_user_id).first() or referees.first()
            )

        cache.set(cache_key, next_referee.id, timeout=24 * 60 * 60)
        return next_referee


class RoundRobinProcess(Process):
    match_details = jsonstore.CharField(max_length=500)
    umpired = jsonstore.BooleanField(default=False)

    class Meta:
        proxy = True

    def __str__(self):
        return f"RoundRobinProcess: {self.match_details[:50]}"


class RoundRobinFlow(flow.Flow):
    process_class = RoundRobinProcess

    start = (
        flow.Start(CreateProcessView.as_view(fields=["match_details"]))
        .Annotation(title="Submit Match Details")
        .Permission(auto_create=True)
        .Next(this.umpire_match)
    )

    umpire_match = (
        flow.View(UpdateProcessView.as_view(fields=["umpired"]))
        .Annotation(title="Umpire Match")
        .Assign(lambda act: get_next_referee())
        .Next(this.end)
    )

    end = flow.End()

    process_description = "This process assigns tasks to resources in a round-robin manner, ensuring fair and equal task distribution."

    def __str__(self):
        return "Round Robin Allocation Flow"


class TestRoundRobinFlow(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create referee group and users
        cls.referees = [
            User.objects.create_user(username=f"referee{i}", password="password")
            for i in range(1, 4)
        ]
        for referee in cls.referees:
            referee.groups.create(name="Referees")

    def test_flow(self):
        # Start the process and submit match details
        response = self.client.post(
            RoundRobinFlow.start.reverse("execute"),
            {"match_details": "Match 1: Team A vs Team B"},
        )
        self.assertEqual(response.status_code, 302)

        # Get the process and verify the first referee is assigned
        process = RoundRobinProcess.objects.get()
        umpire_task = process.task_set.get(flow_task=RoundRobinFlow.umpire_match)
        self.assertEqual(umpire_task.owner, get_next_referee())

        # Complete the umpiring task
        self.client.login(username="referee1", password="password")
        self.client.post(umpire_task.reverse("assign"), {})
        response = self.client.post(umpire_task.reverse("execute"), {"umpired": True})
        self.assertEqual(response.status_code, 302)

        # Verify the task is marked as completed
        process.refresh_from_db()
        self.assertTrue(process.umpired)

        # Start another process and verify the next referee is assigned
        response = self.client.post(
            RoundRobinFlow.start.reverse("execute"),
            {"match_details": "Match 2: Team C vs Team D"},
        )
        self.assertEqual(response.status_code, 302)

        process = RoundRobinProcess.objects.last()
        umpire_task = process.task_set.get(flow_task=RoundRobinFlow.umpire_match)
        self.assertEqual(umpire_task.owner, get_next_referee())
