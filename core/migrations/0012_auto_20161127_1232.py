# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-11-27 18:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20161023_0847'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalmember',
            name='payment_method',
        ),
        migrations.RemoveField(
            model_name='historicalmember',
            name='show_email',
        ),
        migrations.RemoveField(
            model_name='historicalmember',
            name='stripe_save_card',
        ),
        migrations.RemoveField(
            model_name='member',
            name='payment_method',
        ),
        migrations.RemoveField(
            model_name='member',
            name='show_email',
        ),
        migrations.RemoveField(
            model_name='member',
            name='stripe_save_card',
        ),
    ]