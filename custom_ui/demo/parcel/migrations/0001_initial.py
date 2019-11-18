# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewflow', '0005_rename_flowcls'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryProcess',
            fields=[
                ('process_ptr', models.OneToOneField(on_delete=models.CASCADE, auto_created=True, serialize=False, parent_link=True, to='viewflow.Process', primary_key=True)),
                ('planet', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('approved', models.BooleanField(default=False)),
                ('approved_at', models.DateTimeField(null=True)),
                ('drop_status', models.CharField(null=True, choices=[(b'SCF', b'Successfull'), (b'ERR', b'Unsuccessfull')], max_length=3)),
                ('delivery_report', models.TextField(null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('viewflow.process',),
        ),
    ]
