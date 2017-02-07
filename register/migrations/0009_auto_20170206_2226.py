# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-02-07 04:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0008_auto_20170114_1859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalregistrationgroup',
            name='starting_hole',
            field=models.IntegerField(blank=True, default=1, verbose_name='Starting hole'),
        ),
        migrations.AlterField(
            model_name='historicalregistrationslot',
            name='slot',
            field=models.IntegerField(default=0, verbose_name='Slot number'),
        ),
        migrations.AlterField(
            model_name='registrationgroup',
            name='starting_hole',
            field=models.IntegerField(blank=True, default=1, verbose_name='Starting hole'),
        ),
        migrations.AlterField(
            model_name='registrationslot',
            name='slot',
            field=models.IntegerField(default=0, verbose_name='Slot number'),
        ),
    ]