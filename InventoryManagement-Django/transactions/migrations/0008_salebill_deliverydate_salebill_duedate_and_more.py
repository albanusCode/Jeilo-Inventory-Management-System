# Generated by Django 4.2.2 on 2023-07-21 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0007_salebill_shipm'),
    ]

    operations = [
        migrations.AddField(
            model_name='salebill',
            name='deliveryDate',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AddField(
            model_name='salebill',
            name='dueDate',
            field=models.CharField(default=' ', max_length=150),
        ),
        migrations.AddField(
            model_name='salebill',
            name='paymentTerms',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AddField(
            model_name='salebill',
            name='shipt',
            field=models.CharField(default='', max_length=150),
        ),
    ]
