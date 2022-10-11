# Generated by Django 3.2.9 on 2021-12-03 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('viewflow', '0010_viewflow20'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Insurance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=50)),
                ('cost', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipment_no', models.CharField(max_length=50)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.CharField(max_length=150)),
                ('city', models.CharField(max_length=150)),
                ('state', models.CharField(max_length=150)),
                ('zipcode', models.CharField(max_length=10)),
                ('country', models.CharField(max_length=150)),
                ('phone', models.CharField(max_length=50)),
                ('need_insurance', models.BooleanField(default=False)),
                ('carrier_quote', models.IntegerField(default=0)),
                ('post_label', models.TextField(blank=True, null=True)),
                ('package_tag', models.CharField(max_length=50)),
                ('carrier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shipment.carrier')),
                ('insurance', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shipment.insurance')),
            ],
        ),
        migrations.CreateModel(
            name='ShipmentProcess',
            fields=[
            ],
            options={
                'verbose_name_plural': 'Shipment process list',
                'permissions': [('can_start_request', 'Can start shipment request'), ('can_take_extra_insurance', 'Can take extra insurance'), ('can_package_goods', 'Can package goods'), ('can_move_package', 'Can move package')],
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('viewflow.process',),
        ),
        migrations.CreateModel(
            name='ShipmentItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('quantity', models.IntegerField(default=1)),
                ('shipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shipment.shipment')),
            ],
        ),
    ]
