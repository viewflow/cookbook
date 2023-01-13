from django.utils.translation import gettext_lazy as _

from viewflow import this
from viewflow.workflow import act, flow

from . import views, models


class BloodTestFlow(flow.Flow):
    process_class = models.BloodTestProcess
    process_title = _("Blood test")

    first_sample = flow.Start(views.FirstBloodSampleView.as_view()).Next(
        this.biochemical_analysis
    )

    second_sample = flow.Start(views.second_blood_sample).Next(
        this.biochemical_analysis
    )

    biochemical_analysis = flow.View(views.biochemical_data).Next(this.split_analysis)

    split_analysis = (
        flow.Split()
        .Next(this.hormone_tests, case=act.process.hormone_test_required)
        .Next(this.tumor_markers_test, case=act.process.tumor_test_required)
        .Next(this.join_analysis)
    )

    hormone_tests = flow.View(views.HormoneTestFormView.as_view()).Next(
        this.join_analysis
    )

    tumor_markers_test = (
        flow.View(
            views.GenericTestFormView.as_view(
                model=models.TumorMarkers,
                template_name="viewflow//workflow/task.html",
                fields=[
                    "alpha_fetoprotein",
                    "beta_gonadotropin",
                    "ca19",
                    "cea",
                    "pap",
                    "pas",
                ],
            )
        )
        .Annotation(title="Tumor Markers Test")
        .Next(this.join_analysis)
    )

    join_analysis = flow.Join().Next(this.end)

    end = flow.End()
