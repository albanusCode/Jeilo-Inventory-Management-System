# Generated by Django 4.2.2 on 2023-07-20 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0006_remove_purchasebilldetails_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='salebill',
            name='shipm',
            field=models.CharField(default='', max_length=150),
        ),
    ]
