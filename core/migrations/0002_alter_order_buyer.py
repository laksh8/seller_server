# Generated by Django 5.1.6 on 2025-05-06 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='buyer',
            field=models.CharField(max_length=100),
        ),
    ]
