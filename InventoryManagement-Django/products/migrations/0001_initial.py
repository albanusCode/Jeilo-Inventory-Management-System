# Generated by Django 3.0.7 on 2023-06-16 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('type', models.CharField(max_length=50)),
                ('quantity', models.PositiveIntegerField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
    ]
