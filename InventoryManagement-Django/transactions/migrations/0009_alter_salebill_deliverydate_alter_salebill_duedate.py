# Generated by Django 4.2.2 on 2023-07-21 09:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0008_salebill_deliverydate_salebill_duedate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salebill',
            name='deliveryDate',
            field=models.DateField(default=datetime.date.today, max_length=150),
        ),
        migrations.AlterField(
            model_name='salebill',
            name='dueDate',
            field=models.DateField(default=datetime.date.today, max_length=150),
        ),
    ]
