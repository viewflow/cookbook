from django.db import models


class TaskCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class TaskSubcategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        TaskCategory, on_delete=models.CASCADE, related_name="subcategories"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Subcategories"


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(TaskCategory, on_delete=models.SET_NULL, null=True)
    subcategory = models.ForeignKey(
        TaskSubcategory, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return f"{self.name} ({self.project.name})"
