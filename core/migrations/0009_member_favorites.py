# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-30 13:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20160630_0847'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='favorites',
            field=models.ManyToManyField(blank=True, related_name='_member_favorites_+', to='core.Member'),
        ),
    ]
