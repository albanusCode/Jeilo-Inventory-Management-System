# Generated by Django 4.2.2 on 2023-08-02 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0013_alter_stock_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='value',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=8),
        ),
    ]
