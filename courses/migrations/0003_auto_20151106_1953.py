# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_historicalcourse_historicalcoursesetup_historicalcoursesetuphole_historicalhole'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursesetup',
            name='rating',
            field=models.DecimalField(max_digits=4, null=True, blank=True, decimal_places=1),
        ),
        migrations.AlterField(
            model_name='coursesetup',
            name='slope',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalcoursesetup',
            name='rating',
            field=models.DecimalField(max_digits=4, null=True, blank=True, decimal_places=1),
        ),
        migrations.AlterField(
            model_name='historicalcoursesetup',
            name='slope',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalhole',
            name='default_handicap',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='hole',
            name='default_handicap',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
