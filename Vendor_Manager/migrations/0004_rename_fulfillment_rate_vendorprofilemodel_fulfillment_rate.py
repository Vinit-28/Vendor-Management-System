# Generated by Django 4.2.7 on 2023-12-10 19:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Vendor_Manager', '0003_alter_historicalperformancesmodel_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vendorprofilemodel',
            old_name='fulfillment_Rate',
            new_name='fulfillment_rate',
        ),
    ]
