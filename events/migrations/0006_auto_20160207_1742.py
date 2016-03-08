# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-07 23:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20160207_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='skins_type',
            field=models.CharField(choices=[('I', 'Individual'), ('T', 'Team'), ('N', 'No Skins')], default='N', max_length=1, verbose_name='Skins type'),
        ),
        migrations.AddField(
            model_name='eventtemplate',
            name='skins_type',
            field=models.CharField(choices=[('I', 'Individual'), ('T', 'Team'), ('N', 'No Skins')], default='N', max_length=1, verbose_name='Skins type'),
        ),
        migrations.AddField(
            model_name='historicalevent',
            name='skins_type',
            field=models.CharField(choices=[('I', 'Individual'), ('T', 'Team'), ('N', 'No Skins')], default='N', max_length=1, verbose_name='Skins type'),
        ),
        migrations.AddField(
            model_name='historicaleventtemplate',
            name='skins_type',
            field=models.CharField(choices=[('I', 'Individual'), ('T', 'Team'), ('N', 'No Skins')], default='N', max_length=1, verbose_name='Skins type'),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.CharField(choices=[('L', 'League'), ('M', 'Weekend Major'), ('H', 'Holiday Pro-shop Event'), ('O', 'Other')], default='M', max_length=1, verbose_name='Event type'),
        ),
        migrations.AlterField(
            model_name='event',
            name='scoring',
            field=models.CharField(choices=[('IN', 'Individual'), ('TBB', 'Team: Best Ball'), ('TAG', 'Team: Aggregate Score'), ('TS', 'Team: Scramble'), ('TA', 'Team: Alternate Shot'), ('TC', 'Team: Combination')], default='IN', max_length=3, verbose_name='Scoring type'),
        ),
        migrations.AlterField(
            model_name='eventtemplate',
            name='event_type',
            field=models.CharField(choices=[('L', 'League'), ('M', 'Weekend Major'), ('H', 'Holiday Pro-shop Event'), ('O', 'Other')], default='M', max_length=1, verbose_name='Event type'),
        ),
        migrations.AlterField(
            model_name='eventtemplate',
            name='scoring',
            field=models.CharField(choices=[('IN', 'Individual'), ('TBB', 'Team: Best Ball'), ('TAG', 'Team: Aggregate Score'), ('TS', 'Team: Scramble'), ('TA', 'Team: Alternate Shot'), ('TC', 'Team: Combination')], default='IN', max_length=3, verbose_name='Scoring type'),
        ),
        migrations.AlterField(
            model_name='historicalevent',
            name='event_type',
            field=models.CharField(choices=[('L', 'League'), ('M', 'Weekend Major'), ('H', 'Holiday Pro-shop Event'), ('O', 'Other')], default='M', max_length=1, verbose_name='Event type'),
        ),
        migrations.AlterField(
            model_name='historicalevent',
            name='scoring',
            field=models.CharField(choices=[('IN', 'Individual'), ('TBB', 'Team: Best Ball'), ('TAG', 'Team: Aggregate Score'), ('TS', 'Team: Scramble'), ('TA', 'Team: Alternate Shot'), ('TC', 'Team: Combination')], default='IN', max_length=3, verbose_name='Scoring type'),
        ),
        migrations.AlterField(
            model_name='historicaleventtemplate',
            name='event_type',
            field=models.CharField(choices=[('L', 'League'), ('M', 'Weekend Major'), ('H', 'Holiday Pro-shop Event'), ('O', 'Other')], default='M', max_length=1, verbose_name='Event type'),
        ),
        migrations.AlterField(
            model_name='historicaleventtemplate',
            name='scoring',
            field=models.CharField(choices=[('IN', 'Individual'), ('TBB', 'Team: Best Ball'), ('TAG', 'Team: Aggregate Score'), ('TS', 'Team: Scramble'), ('TA', 'Team: Alternate Shot'), ('TC', 'Team: Combination')], default='IN', max_length=3, verbose_name='Scoring type'),
        ),
    ]
