from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from viewflow.workflow.models import Process


class Patient(models.Model):
    patient_id = models.CharField(max_length=250)
    age = models.IntegerField()
    sex = models.CharField(
        max_length=1,
        choices=(
            ("M", "Male"),
            ("F", "Female"),
            ("O", "Other"),
            ("U", "Unknown")))
    weight = models.DecimalField(
        max_digits=4, decimal_places=1,
        help_text='kg')
    height = models.IntegerField(help_text="cm")
    comment = models.TextField(blank=True)

    def __str__(self):
        return self.patient_id


class BloodSample(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    taken_at = models.DateTimeField(default=timezone.now)
    taken_by = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)


class Biochemistry(models.Model):
    sample = models.OneToOneField(BloodSample, on_delete=models.CASCADE)
    hemoglobin = models.IntegerField(help_text='g/dL')
    lymphocytes = models.DecimalField(max_digits=3, decimal_places=1, help_text='10^9/L')


class TumorMarkers(models.Model):
    sample = models.OneToOneField(BloodSample, on_delete=models.CASCADE)
    alpha_fetoprotein = models.IntegerField(help_text='ng/mL')
    beta_gonadotropin = models.IntegerField(help_text='IU/I')
    ca19 = models.IntegerField(help_text='U/mL')
    cea = models.IntegerField(help_text='ug/L')
    pap = models.IntegerField(help_text='U/dL')
    pas = models.IntegerField(help_text='ug/L')


class Hormones(models.Model):
    sample = models.OneToOneField(BloodSample, on_delete=models.CASCADE)
    acth = models.DecimalField(max_digits=3, decimal_places=1, help_text='pmol/L')
    estradiol = models.IntegerField(help_text='ng/dL')
    free_t3 = models.DecimalField(max_digits=3, decimal_places=1, help_text='ng/dL')
    free_t4 = models.IntegerField(help_text='pmol/L')


class BloodTestProcess(Process):
    class Meta:
        proxy = True

    @property
    def tumor_test_required(self):
        return self.artefact.biochemistry.lymphocytes > 5

    @property
    def hormone_test_required(self):
        return self.artefact.biochemistry.hemoglobin < 12
