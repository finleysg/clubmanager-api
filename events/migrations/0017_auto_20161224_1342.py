# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-12-24 19:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0016_auto_20161030_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.CharField(choices=[('L', 'League'), ('W', 'Weekend Major'), ('H', 'Holiday Pro-shop Event'), ('M', 'Member Meeting'), ('B', 'Board Meeting'), ('O', 'Other'), ('S', 'State Tournament'), ('R', 'Open Registration Period')], default='L', max_length=1, verbose_name='Event type'),
        ),
        migrations.AlterField(
            model_name='eventtemplate',
            name='event_type',
            field=models.CharField(choices=[('L', 'League'), ('W', 'Weekend Major'), ('H', 'Holiday Pro-shop Event'), ('M', 'Member Meeting'), ('B', 'Board Meeting'), ('O', 'Other'), ('S', 'State Tournament'), ('R', 'Open Registration Period')], default='L', max_length=1, verbose_name='Event type'),
        ),
        migrations.AlterField(
            model_name='historicalevent',
            name='event_type',
            field=models.CharField(choices=[('L', 'League'), ('W', 'Weekend Major'), ('H', 'Holiday Pro-shop Event'), ('M', 'Member Meeting'), ('B', 'Board Meeting'), ('O', 'Other'), ('S', 'State Tournament'), ('R', 'Open Registration Period')], default='L', max_length=1, verbose_name='Event type'),
        ),
        migrations.AlterField(
            model_name='historicaleventtemplate',
            name='event_type',
            field=models.CharField(choices=[('L', 'League'), ('W', 'Weekend Major'), ('H', 'Holiday Pro-shop Event'), ('M', 'Member Meeting'), ('B', 'Board Meeting'), ('O', 'Other'), ('S', 'State Tournament'), ('R', 'Open Registration Period')], default='L', max_length=1, verbose_name='Event type'),
        ),
    ]
