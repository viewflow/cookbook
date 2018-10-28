from viewflow import flow, frontend
from viewflow.base import this, Flow

from . import views, models


@frontend.register
class BloodTestFlow(Flow):
    process_class = models.BloodTestProcess

    first_sample = flow.Start(
        views.FirstBloodSampleView
    ).Next(this.biochemical_analysis)

    second_sample = flow.Start(
        views.second_blood_sample
    ).Next(this.biochemical_analysis)

    biochemical_analysis = flow.View(
        views.biochemical_data
    ).Next(this.split_analysis)

    split_analysis = (
        flow.Split()
        .Next(
            this.hormone_tests,
            cond=lambda act: act.process.hormone_test_required
        ).Next(
            this.tumor_markers_test,
            cond=lambda act: act.process.tumor_test_required
        ).Next(
            this.join_analysis
        )
    )

    hormone_tests = flow.View(
        views.HormoneTestFormView
    ).Next(this.join_analysis)

    tumor_markers_test = flow.View(
        views.GenericTestFormView,
        model=models.TumorMarkers,
        fields=[
            'alpha_fetoprotein', 'beta_gonadotropin', 'ca19',
            'cea', 'pap', 'pas'
        ],
        task_description='Tumor Markers Test'
    ).Next(this.join_analysis)

    join_analysis = flow.Join().Next(this.end)

    end = flow.End()
