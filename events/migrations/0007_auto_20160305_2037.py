# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-06 02:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20160207_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='end_date',
            field=models.DateField(blank=True, null=True, verbose_name='End date (multi-day events)'),
        ),
        migrations.AlterField(
            model_name='event',
            name='end_time',
            field=models.TimeField(blank=True, null=True, verbose_name='Ending time (non-shotgun starts)'),
        ),
        migrations.AlterField(
            model_name='historicalevent',
            name='end_date',
            field=models.DateField(blank=True, null=True, verbose_name='End date (multi-day events)'),
        ),
        migrations.AlterField(
            model_name='historicalevent',
            name='end_time',
            field=models.TimeField(blank=True, null=True, verbose_name='Ending time (non-shotgun starts)'),
        ),
    ]
