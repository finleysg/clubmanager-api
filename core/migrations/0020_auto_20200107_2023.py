# Generated by Django 2.1.7 on 2020-01-08 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20181210_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalmember',
            name='ghin',
            field=models.CharField(blank=True, max_length=8, null=True, verbose_name='GHIN'),
        ),
        migrations.AlterField(
            model_name='member',
            name='ghin',
            field=models.CharField(blank=True, max_length=8, null=True, verbose_name='GHIN'),
        ),
    ]
