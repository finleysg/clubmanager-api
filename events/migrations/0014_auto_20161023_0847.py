# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-10-23 13:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_auto_20160622_1246'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='external_url',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='External url'),
        ),
        migrations.AddField(
            model_name='event',
            name='requires_registration',
            field=models.BooleanField(default=True, verbose_name='Requires registration'),
        ),
        migrations.AddField(
            model_name='eventtemplate',
            name='external_url',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='External url'),
        ),
        migrations.AddField(
            model_name='eventtemplate',
            name='requires_registration',
            field=models.BooleanField(default=True, verbose_name='Requires registration'),
        ),
        migrations.AddField(
            model_name='historicalevent',
            name='external_url',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='External url'),
        ),
        migrations.AddField(
            model_name='historicalevent',
            name='requires_registration',
            field=models.BooleanField(default=True, verbose_name='Requires registration'),
        ),
        migrations.AddField(
            model_name='historicaleventtemplate',
            name='external_url',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='External url'),
        ),
        migrations.AddField(
            model_name='historicaleventtemplate',
            name='requires_registration',
            field=models.BooleanField(default=True, verbose_name='Requires registration'),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.CharField(choices=[('L', 'League'), ('W', 'Weekend Major'), ('H', 'Holiday Pro-shop Event'), ('M', 'Member Meeting'), ('B', 'Board Meeting'), ('O', 'Other')], default='L', max_length=1, verbose_name='Event type'),
        ),
        migrations.AlterField(
            model_name='event',
            name='scoring',
            field=models.CharField(choices=[('IN', 'Individual'), ('TBB', 'Team: Best Ball'), ('TAG', 'Team: Aggregate Score'), ('TS', 'Team: Scramble'), ('TA', 'Team: Alternate Shot'), ('TC', 'Team: Combination'), ('NA', 'Not Applicable')], default='NA', max_length=3, verbose_name='Scoring type'),
        ),
        migrations.AlterField(
            model_name='event',
            name='scoring_system',
            field=models.CharField(choices=[('SP', 'Stroke Play'), ('SF', 'Stableford'), ('CH', 'Chicago'), ('NA', 'Not Applicable')], default='NA', max_length=2, verbose_name='Scoring system'),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_type',
            field=models.CharField(choices=[('TT', 'Tee Times'), ('FB', 'Front and Back'), ('SG', 'Shotgun'), ('NA', 'Not Applicable')], default='NA', max_length=2, verbose_name='Start type'),
        ),
        migrations.AlterField(
            model_name='eventtemplate',
            name='event_type',
            field=models.CharField(choices=[('L', 'League'), ('W', 'Weekend Major'), ('H', 'Holiday Pro-shop Event'), ('M', 'Member Meeting'), ('B', 'Board Meeting'), ('O', 'Other')], default='L', max_length=1, verbose_name='Event type'),
        ),
        migrations.AlterField(
            model_name='eventtemplate',
            name='scoring',
            field=models.CharField(choices=[('IN', 'Individual'), ('TBB', 'Team: Best Ball'), ('TAG', 'Team: Aggregate Score'), ('TS', 'Team: Scramble'), ('TA', 'Team: Alternate Shot'), ('TC', 'Team: Combination'), ('NA', 'Not Applicable')], default='NA', max_length=3, verbose_name='Scoring type'),
        ),
        migrations.AlterField(
            model_name='eventtemplate',
            name='scoring_system',
            field=models.CharField(choices=[('SP', 'Stroke Play'), ('SF', 'Stableford'), ('CH', 'Chicago'), ('NA', 'Not Applicable')], default='NA', max_length=2, verbose_name='Scoring system'),
        ),
        migrations.AlterField(
            model_name='eventtemplate',
            name='start_type',
            field=models.CharField(choices=[('TT', 'Tee Times'), ('FB', 'Front and Back'), ('SG', 'Shotgun'), ('NA', 'Not Applicable')], default='NA', max_length=2, verbose_name='Start type'),
        ),
        migrations.AlterField(
            model_name='historicalevent',
            name='event_type',
            field=models.CharField(choices=[('L', 'League'), ('W', 'Weekend Major'), ('H', 'Holiday Pro-shop Event'), ('M', 'Member Meeting'), ('B', 'Board Meeting'), ('O', 'Other')], default='L', max_length=1, verbose_name='Event type'),
        ),
        migrations.AlterField(
            model_name='historicalevent',
            name='scoring',
            field=models.CharField(choices=[('IN', 'Individual'), ('TBB', 'Team: Best Ball'), ('TAG', 'Team: Aggregate Score'), ('TS', 'Team: Scramble'), ('TA', 'Team: Alternate Shot'), ('TC', 'Team: Combination'), ('NA', 'Not Applicable')], default='NA', max_length=3, verbose_name='Scoring type'),
        ),
        migrations.AlterField(
            model_name='historicalevent',
            name='scoring_system',
            field=models.CharField(choices=[('SP', 'Stroke Play'), ('SF', 'Stableford'), ('CH', 'Chicago'), ('NA', 'Not Applicable')], default='NA', max_length=2, verbose_name='Scoring system'),
        ),
        migrations.AlterField(
            model_name='historicalevent',
            name='start_type',
            field=models.CharField(choices=[('TT', 'Tee Times'), ('FB', 'Front and Back'), ('SG', 'Shotgun'), ('NA', 'Not Applicable')], default='NA', max_length=2, verbose_name='Start type'),
        ),
        migrations.AlterField(
            model_name='historicaleventtemplate',
            name='event_type',
            field=models.CharField(choices=[('L', 'League'), ('W', 'Weekend Major'), ('H', 'Holiday Pro-shop Event'), ('M', 'Member Meeting'), ('B', 'Board Meeting'), ('O', 'Other')], default='L', max_length=1, verbose_name='Event type'),
        ),
        migrations.AlterField(
            model_name='historicaleventtemplate',
            name='scoring',
            field=models.CharField(choices=[('IN', 'Individual'), ('TBB', 'Team: Best Ball'), ('TAG', 'Team: Aggregate Score'), ('TS', 'Team: Scramble'), ('TA', 'Team: Alternate Shot'), ('TC', 'Team: Combination'), ('NA', 'Not Applicable')], default='NA', max_length=3, verbose_name='Scoring type'),
        ),
        migrations.AlterField(
            model_name='historicaleventtemplate',
            name='scoring_system',
            field=models.CharField(choices=[('SP', 'Stroke Play'), ('SF', 'Stableford'), ('CH', 'Chicago'), ('NA', 'Not Applicable')], default='NA', max_length=2, verbose_name='Scoring system'),
        ),
        migrations.AlterField(
            model_name='historicaleventtemplate',
            name='start_type',
            field=models.CharField(choices=[('TT', 'Tee Times'), ('FB', 'Front and Back'), ('SG', 'Shotgun'), ('NA', 'Not Applicable')], default='NA', max_length=2, verbose_name='Start type'),
        ),
    ]