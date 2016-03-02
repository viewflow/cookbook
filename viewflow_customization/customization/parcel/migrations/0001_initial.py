# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import viewflow.token
import viewflow.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Parcel',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Planet',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=150)),
                ('distance', models.IntegerField()),
            ],
            options={
                'permissions': [('land_on_planet', 'Can land on planet')],
            },
        ),
        migrations.CreateModel(
            name='ShipmentItem',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=250)),
                ('quantity', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='ShipmentProcess',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('flow_cls', viewflow.fields.FlowReferenceField(max_length=250)),
                ('status', models.CharField(max_length=50, default='NEW')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('finished', models.DateTimeField(null=True, blank=True)),
                ('approved', models.BooleanField(default=False)),
                ('deliver_report', models.TextField(null=True)),
                ('parcel', models.ForeignKey(to='parcel.Parcel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ShipmentTask',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('flow_task', viewflow.fields.TaskReferenceField(max_length=150)),
                ('flow_task_type', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=50, default='NEW', db_index=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('started', models.DateTimeField(null=True, blank=True)),
                ('finished', models.DateTimeField(null=True, blank=True)),
                ('token', viewflow.fields.TokenField(max_length=150, default=viewflow.token.Token('start'))),
                ('owner_permission', models.CharField(max_length=50, null=True, blank=True)),
                ('owner', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('previous', models.ManyToManyField(related_name='leading', to='parcel.ShipmentTask')),
                ('process', models.ForeignKey(to='parcel.ShipmentProcess')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='shipmentitem',
            name='shipment',
            field=models.ForeignKey(to='parcel.ShipmentProcess'),
        ),
        migrations.AddField(
            model_name='parcel',
            name='planet',
            field=models.ForeignKey(to='parcel.Planet'),
        ),
    ]
