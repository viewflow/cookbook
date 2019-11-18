# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewflow', '0004_subprocess'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerVerificationProcess',
            fields=[
                ('subprocess_ptr', models.OneToOneField(on_delete=models.CASCADE, parent_link=True, auto_created=True, to='viewflow.Subprocess', serialize=False, primary_key=True)),
                ('trusted', models.NullBooleanField()),
            ],
            options={
                'abstract': False,
            },
            bases=('viewflow.subprocess',),
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('quantity', models.IntegerField(default=1)),
                ('reserved', models.NullBooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='OrderItemProcess',
            fields=[
                ('subprocess_ptr', models.OneToOneField(on_delete=models.CASCADE, parent_link=True, auto_created=True, to='viewflow.Subprocess', serialize=False, primary_key=True)),
                ('item', models.ForeignKey(to='order.OrderItem', on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=('viewflow.subprocess',),
        ),
        migrations.CreateModel(
            name='OrderProcess',
            fields=[
                ('process_ptr', models.OneToOneField(on_delete=models.CASCADE, parent_link=True, auto_created=True, to='viewflow.Process', serialize=False, primary_key=True)),
                ('customer_name', models.CharField(max_length=250)),
                ('customer_address', models.CharField(max_length=250)),
            ],
            options={
                'abstract': False,
            },
            bases=('viewflow.process',),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(to='order.OrderProcess', on_delete=models.CASCADE),
        ),
    ]
