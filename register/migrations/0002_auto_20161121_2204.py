# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-11-22 04:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signupslot',
            name='registration_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='slots', to='register.RegistrationGroup', verbose_name='Group'),
        ),
    ]
