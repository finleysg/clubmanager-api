# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-18 14:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_auto_20160305_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='start_time',
            field=models.CharField(max_length=40, verbose_name='Starting time'),
        ),
        migrations.AlterField(
            model_name='historicalevent',
            name='start_time',
            field=models.CharField(max_length=40, verbose_name='Starting time'),
        ),
    ]
