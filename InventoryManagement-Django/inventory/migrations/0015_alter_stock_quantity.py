# Generated by Django 4.2.2 on 2023-08-02 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0014_alter_stock_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
