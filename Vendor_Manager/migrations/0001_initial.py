# Generated by Django 4.2.7 on 2023-11-29 10:45

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vendors',
            fields=[
                ('vendor_code', models.CharField(max_length=256, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256, null=True)),
                ('contact_details', models.CharField(max_length=20, null=True)),
                ('address', models.TextField()),
                ('on_time_delivery_rate', models.FloatField(default=0)),
                ('quality_rating_avg', models.FloatField(default=0)),
                ('average_response_time', models.FloatField(default=0)),
                ('fulfillment_Rate', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseOrders',
            fields=[
                ('po_number', models.CharField(max_length=512, primary_key=True, serialize=False)),
                ('order_date', models.DateField(default=datetime.date.today)),
                ('expected_delivery_date', models.DateField()),
                ('delivery_date', models.DateField(null=True)),
                ('items', models.JSONField()),
                ('quantity', models.IntegerField()),
                ('status', models.CharField(default='pending', max_length=32)),
                ('quality_rating', models.FloatField(null=True)),
                ('issue_date', models.DateTimeField()),
                ('acknowledgment_date', models.DateTimeField(null=True)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Vendor_Manager.vendors')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalPerformances',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('on_time_delivery_rate', models.FloatField(default=0)),
                ('quality_rating_avg', models.FloatField(default=0)),
                ('average_response_time', models.FloatField(default=0)),
                ('fulfillment_rate', models.FloatField(default=0)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Vendor_Manager.vendors')),
            ],
        ),
    ]
