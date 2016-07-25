# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-30 13:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20160604_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalmember',
            name='parent',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.HistoricalMember'),
        ),
        migrations.AddField(
            model_name='member',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='core.Member'),
        ),
    ]
