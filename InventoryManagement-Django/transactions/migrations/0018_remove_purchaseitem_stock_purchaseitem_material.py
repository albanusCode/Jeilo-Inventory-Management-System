# Generated by Django 4.2.2 on 2023-08-01 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0017_alter_purchaseitem_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchaseitem',
            name='stock',
        ),
        migrations.AddField(
            model_name='purchaseitem',
            name='material',
            field=models.CharField(default='', max_length=150),
        ),
    ]