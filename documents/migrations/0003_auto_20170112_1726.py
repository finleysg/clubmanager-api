# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-01-12 23:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_auto_20161121_2036'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='year',
            field=models.IntegerField(default=0, verbose_name='Golf Season'),
        ),
        migrations.AddField(
            model_name='historicaldocument',
            name='year',
            field=models.IntegerField(default=0, verbose_name='Golf Season'),
        ),
    ]
