# Generated by Django 4.2.2 on 2023-07-19 07:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_rename_kra_salebill_mode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchasebilldetails',
            name='id',
        ),
        migrations.AlterField(
            model_name='purchasebill',
            name='billno',
            field=models.CharField(editable=False, max_length=4, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='purchasebilldetails',
            name='billno',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='saledetailsbillno', serialize=False, to='transactions.purchasebill'),
        ),
    ]