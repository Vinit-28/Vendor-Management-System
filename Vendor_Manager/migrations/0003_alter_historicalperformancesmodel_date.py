# Generated by Django 4.2.7 on 2023-12-09 18:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vendor_Manager', '0002_rename_historicalperformances_historicalperformancesmodel_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalperformancesmodel',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
