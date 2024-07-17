"""
Description:
    A loop lets you do a task repeatedly. It checks a condition either at the
    start (pre-test) or at the end (post-test) to see if the loop should
    continue. The loop has one entry and exit point.

Examples:
    Keep selecting players until the whole team is chosen.

Motivation:
    There are two main types of loops:

    While Loop: This loop repeats a task zero or more times as long as a
    condition is true. It checks the condition before each loop iteration. If
    the condition is false, it stops and moves to the next task.

    Repeat Loop: This loop repeats a task one or more times until a condition is
    true. It checks the condition after each loop iteration. If the condition is
    true, it stops and moves to the next task."""

from django import forms
from django.shortcuts import render, redirect
from django.core.validators import MaxValueValidator, MinValueValidator
from viewflow import this, jsonstore
from viewflow.forms import Form
from viewflow.workflow import act, flow
from viewflow.workflow.models import Process
from viewflow.workflow.flow import views


class PlayerSelectionProcess(Process):
    players_selected = jsonstore.JSONField(default=list)
    team_size = jsonstore.IntegerField(
        validators=[MinValueValidator(2), MaxValueValidator(6)]
    )

    @property
    def created_by(self):
        """Lookup for the owner of the task that started the flow."""
        return self.flow_class.task_class._default_manager.get(
            process=self, flow_task_type="HUMAN_START"
        ).owner

    class Meta:
        proxy = True


class PlayetSelectionForm(Form):
    player = forms.ChoiceField(choices=())

    def __init__(self, *args, players_selected=None, **kwargs):
        super().__init__(*args, **kwargs)
        all_players = [(str(i), f"Player {i}") for i in range(1, 11)]
        if players_selected:
            available_players = [
                player for player in all_players if player[0] not in players_selected
            ]
        else:
            available_players = all_players

        self.fields["player"].choices = available_players


def select_player_view(request, **kwargs):
    process = request.activation.process
    form = PlayetSelectionForm(
        request.POST or None,
        players_selected=process.players_selected,
    )

    if form.is_valid():
        process.players_selected = [
            form.cleaned_data["player"]
        ] + process.players_selected
        process.save(update_fields=["data"])

        # View is workflow independed and can be used in different flows.
        request.activation.execute()

        # Redirect to the next avaialbe task
        return redirect(request.activation.get_success_url(request))

    return render(request, "viewflow/workflow/task.html", {"form": form})


class Loop(flow.Flow):
    process_class = PlayerSelectionProcess

    start = flow.Start(views.CreateProcessView.as_view(fields=["team_size"])).Next(
        this.select_player
    )

    select_player = (
        flow.View(select_player_view)
        .Assign(act.process.created_by)
        .Next(this.check_if_done)
    )

    check_if_done = (
        flow.If(lambda act: len(act.process.players_selected) < act.process.team_size)
        .Then(this.select_player)
        .Else(this.end)
    )

    end = flow.End()

    process_description = (
        "A loop lets you do a task repeatedly. It checks a condition either at the "
        "start (pre-test) or at the end (post-test) to see if the loop should "
        "continue. The loop has one entry and exit point."
    )

    def __str__(self) -> str:
        return "Keep selecting players until the whole team is chosen."
