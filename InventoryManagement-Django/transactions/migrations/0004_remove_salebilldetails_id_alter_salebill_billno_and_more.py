# Generated by Django 4.2.2 on 2023-07-19 06:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_saleitem_pqty'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salebilldetails',
            name='id',
        ),
        migrations.AlterField(
            model_name='salebill',
            name='billno',
            field=models.CharField(editable=False, max_length=4, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='salebilldetails',
            name='billno',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='saledetailsbillno', serialize=False, to='transactions.salebill'),
        ),
    ]