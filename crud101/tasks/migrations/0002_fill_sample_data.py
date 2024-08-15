from django.db import migrations


def fill_sample_data(apps, schema_editor):
    TaskCategory = apps.get_model("tasks", "TaskCategory")
    TaskSubcategory = apps.get_model("tasks", "TaskSubcategory")

    # Sample Categories
    dev_category = TaskCategory.objects.create(name="Development")
    marketing_category = TaskCategory.objects.create(name="Marketing")
    hr_category = TaskCategory.objects.create(name="Human Resources")

    # Sample Subcategories
    TaskSubcategory.objects.create(name="Frontend", category=dev_category)
    TaskSubcategory.objects.create(name="Backend", category=dev_category)
    TaskSubcategory.objects.create(name="SEO", category=marketing_category)
    TaskSubcategory.objects.create(name="Content Creation", category=marketing_category)
    TaskSubcategory.objects.create(name="Recruitment", category=hr_category)
    TaskSubcategory.objects.create(name="Employee Relations", category=hr_category)


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(fill_sample_data),
    ]
