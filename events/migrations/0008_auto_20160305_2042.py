# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-06 02:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20160305_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Event title'),
        ),
        migrations.AlterField(
            model_name='historicalevent',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Event title'),
        ),
    ]
