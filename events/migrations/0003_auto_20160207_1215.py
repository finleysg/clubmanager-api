# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-07 18:15
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20151128_1607'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='courses',
        ),
        migrations.RemoveField(
            model_name='event',
            name='is_shotgun_start',
        ),
        migrations.RemoveField(
            model_name='eventtemplate',
            name='is_shotgun_start',
        ),
        migrations.RemoveField(
            model_name='historicalevent',
            name='is_shotgun_start',
        ),
        migrations.RemoveField(
            model_name='historicaleventtemplate',
            name='is_shotgun_start',
        ),
        migrations.AddField(
            model_name='event',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2016, 2, 7, 18, 14, 47, 853830, tzinfo=utc), verbose_name='End date (multi-day events)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='end_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2016, 2, 7, 18, 15, 8, 451333, tzinfo=utc), verbose_name='Ending time (non-shotgun starts)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='notes',
            field=models.TextField(blank=True, verbose_name='Notes'),
        ),
        migrations.AddField(
            model_name='event',
            name='start_type',
            field=models.CharField(choices=[('TT', 'Tee Times'), ('FB', 'Front and Back'), ('SG', 'Shotgun')], default='TT', max_length=2, verbose_name='Start type'),
        ),
        migrations.AddField(
            model_name='eventtemplate',
            name='start_type',
            field=models.CharField(choices=[('TT', 'Tee Times'), ('FB', 'Front and Back'), ('SG', 'Shotgun')], default='TT', max_length=2, verbose_name='Start type'),
        ),
        migrations.AddField(
            model_name='historicalevent',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2016, 2, 7, 18, 15, 23, 209479, tzinfo=utc), verbose_name='End date (multi-day events)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalevent',
            name='end_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2016, 2, 7, 18, 15, 32, 435169, tzinfo=utc), verbose_name='Ending time (non-shotgun starts)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalevent',
            name='notes',
            field=models.TextField(blank=True, verbose_name='Notes'),
        ),
        migrations.AddField(
            model_name='historicalevent',
            name='start_type',
            field=models.CharField(choices=[('TT', 'Tee Times'), ('FB', 'Front and Back'), ('SG', 'Shotgun')], default='TT', max_length=2, verbose_name='Start type'),
        ),
        migrations.AddField(
            model_name='historicaleventtemplate',
            name='start_type',
            field=models.CharField(choices=[('TT', 'Tee Times'), ('FB', 'Front and Back'), ('SG', 'Shotgun')], default='TT', max_length=2, verbose_name='Start type'),
        ),
        migrations.AlterField(
            model_name='event',
            name='can_choose_hole',
            field=models.BooleanField(default=False, verbose_name='Member can choose starting hole'),
        ),
        migrations.AlterField(
            model_name='event',
            name='can_signup_group',
            field=models.BooleanField(default=False, verbose_name='Member can sign up group'),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(verbose_name='Format and rules'),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_fee',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Event fee'),
        ),
        migrations.AlterField(
            model_name='event',
            name='group_size',
            field=models.IntegerField(default=4, verbose_name='Group size'),
        ),
        migrations.AlterField(
            model_name='event',
            name='holes_per_round',
            field=models.IntegerField(default=18, verbose_name='Holes per round'),
        ),
        migrations.AlterField(
            model_name='event',
            name='maximum_signup_group_size',
            field=models.IntegerField(default=1, verbose_name='Maximum sign-up group size'),
        ),
        migrations.AlterField(
            model_name='event',
            name='minimum_signup_group_size',
            field=models.IntegerField(default=1, verbose_name='Minimum sign-up group size'),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Event title'),
        ),
        migrations.AlterField(
            model_name='event',
            name='number_of_scores',
            field=models.IntegerField(blank=True, default=1, verbose_name='Number of scores'),
        ),
        migrations.AlterField(
            model_name='event',
            name='rounds',
            field=models.IntegerField(default=1, verbose_name='Number of rounds'),
        ),
        migrations.AlterField(
            model_name='event',
            name='scoring',
            field=models.CharField(choices=[('IN', 'Individual'), ('T1', 'Team: One Score'), ('TM', 'Team: Multiple Scores')], default='IN', max_length=2, verbose_name='Scoring type'),
        ),
        migrations.AlterField(
            model_name='event',
            name='scoring_system',
            field=models.CharField(choices=[('SP', 'Stroke Play'), ('SF', 'Stableford'), ('CH', 'Chicago')], default='SP', max_length=2, verbose_name='Scoring system'),
        ),
        migrations.AlterField(
            model_name='event',
            name='signup_end',
            field=models.DateTimeField(verbose_name='Signup end'),
        ),
        migrations.AlterField(
            model_name='event',
            name='signup_start',
            field=models.DateTimeField(verbose_name='Signup start'),
        ),
        migrations.AlterField(
            model_name='event',
            name='skins_fee',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, verbose_name='Skins fee'),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateField(verbose_name='Start date'),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_time',
            field=models.TimeField(verbose_name='Starting time'),
        ),
        migrations.AlterField(
            model_name='event',
            name='team_scoring',
            field=models.CharField(choices=[('NA', 'Not a Team Event'), ('BB', 'Best Ball'), ('AGG', 'Aggregate')], default='NA', max_length=2, verbose_name='Team scoring type'),
        ),
        migrations.AlterField(
            model_name='eventtemplate',
            name='can_choose_hole',
            field=models.BooleanField(default=False, verbose_name='Member can choose starting hole'),
        ),
        migrations.AlterField(
            model_name='eventtemplate',
            name='can_signup_group',
            field=models.BooleanField(default=False, verbose_name='Member can sign up group'),
        ),
        migrations.AlterField(
            model_name='eventtemplate',
            name='description',
            field=models.TextField(verbose_name='Format and rules'),
        ),
        migrations.AlterField(
            model_name='eventtemplate',
            name='event_fee',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Event fee'),
        ),
        migrations.AlterField(
            model_name='eventtemplate',
            name='group_size',
            field=models.IntegerField(default=4, verbose_name='Group size'),
        ),
        migrations.AlterField(
            model_name='eventtemplate',
            name='holes_per_round',
            field=models.IntegerField(default=18, verbose_name='Holes per round'),
        ),
        migrations.AlterField(
            model_name='eventtemplate',
            name='maximum_signup_group_size',
            field=models.IntegerField(default=1, verbose_name='Maximum sign-up group size'),
        ),
        migrations.AlterField(
            model_name='eventtemplate',
            name='minimum_signup_group_size',
            field=models.IntegerField(default=1, verbose_name='Minimum sign-up group size'),
        ),
        migrations.AlterField(
            model_name='eventtemplate',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Event title'),
        ),
        migrations.AlterField(
            model_name='eventtemplate',
            name='number_of_scores',
            field=models.IntegerField(blank=True, default=1, verbose_name='Number of scores'),
        ),
        migrations.AlterField(
            model_name='eventtemplate',
            name='rounds',
            field=models.IntegerField(default=1, verbose_name='Number of rounds'),
        ),
        migrations.AlterField(
            model_name='eventtemplate',
            name='scoring',
            field=models.CharField(choices=[('IN', 'Individual'), ('T1', 'Team: One Score'), ('TM', 'Team: Multiple Scores')], default='IN', max_length=2, verbose_name='Scoring type'),
        ),
        migrations.AlterField(
            model_name='eventtemplate',
            name='scoring_system',
            field=models.CharField(choices=[('SP', 'Stroke Play'), ('SF', 'Stableford'), ('CH', 'Chicago')], default='SP', max_length=2, verbose_name='Scoring system'),
        ),
        migrations.AlterField(
            model_name='eventtemplate',
            name='skins_fee',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, verbose_name='Skins fee'),
        ),
        migrations.AlterField(
            model_name='eventtemplate',
            name='team_scoring',
            field=models.CharField(choices=[('NA', 'Not a Team Event'), ('BB', 'Best Ball'), ('AGG', 'Aggregate')], default='NA', max_length=2, verbose_name='Team scoring type'),
        ),
        migrations.AlterField(
            model_name='historicalevent',
            name='can_choose_hole',
            field=models.BooleanField(default=False, verbose_name='Member can choose starting hole'),
        ),
        migrations.AlterField(
            model_name='historicalevent',
            name='can_signup_group',
            field=models.BooleanField(default=False, verbose_name='Member can sign up group'),
        ),
        migrations.AlterField(
            model_name='historicalevent',
            name='description',
            field=models.TextField(verbose_name='Format and rules'),
        ),
        migrations.AlterField(
            model_name='historicalevent',
            name='event_fee',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Event fee'),
        ),
        migrations.AlterField(
            model_name='historicalevent',
            name='group_size',
            field=models.IntegerField(default=4, verbose_name='Group size'),
        ),
        migrations.AlterField(
            model_name='historicalevent',
            name='holes_per_round',
            field=models.IntegerField(default=18, verbose_name='Holes per round'),
        ),
        migrations.AlterField(
            model_name='historicalevent',
            name='maximum_signup_group_size',
            field=models.IntegerField(default=1, verbose_name='Maximum sign-up group size'),
        ),
        migrations.AlterField(
            model_name='historicalevent',
            name='minimum_signup_group_size',
            field=models.IntegerField(default=1, verbose_name='Minimum sign-up group size'),
        ),
        migrations.AlterField(
            model_name='historicalevent',
            name='name',
            field=models.CharField(db_index=True, max_length=100, verbose_name='Event title'),
        ),
        migrations.AlterField(
            model_name='historicalevent',
            name='number_of_scores',
            field=models.IntegerField(blank=True, default=1, verbose_name='Number of scores'),
        ),
        migrations.AlterField(
            model_name='historicalevent',
            name='rounds',
            field=models.IntegerField(default=1, verbose_name='Number of rounds'),
        ),
        migrations.AlterField(
            model_name='historicalevent',
            name='scoring',
            field=models.CharField(choices=[('IN', 'Individual'), ('T1', 'Team: One Score'), ('TM', 'Team: Multiple Scores')], default='IN', max_length=2, verbose_name='Scoring type'),
        ),
        migrations.AlterField(
            model_name='historicalevent',
            name='scoring_system',
            field=models.CharField(choices=[('SP', 'Stroke Play'), ('SF', 'Stableford'), ('CH', 'Chicago')], default='SP', max_length=2, verbose_name='Scoring system'),
        ),
        migrations.AlterField(
            model_name='historicalevent',
            name='signup_end',
            field=models.DateTimeField(verbose_name='Signup end'),
        ),
        migrations.AlterField(
            model_name='historicalevent',
            name='signup_start',
            field=models.DateTimeField(verbose_name='Signup start'),
        ),
        migrations.AlterField(
            model_name='historicalevent',
            name='skins_fee',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, verbose_name='Skins fee'),
        ),
        migrations.AlterField(
            model_name='historicalevent',
            name='start_date',
            field=models.DateField(verbose_name='Start date'),
        ),
        migrations.AlterField(
            model_name='historicalevent',
            name='start_time',
            field=models.TimeField(verbose_name='Starting time'),
        ),
        migrations.AlterField(
            model_name='historicalevent',
            name='team_scoring',
            field=models.CharField(choices=[('NA', 'Not a Team Event'), ('BB', 'Best Ball'), ('AGG', 'Aggregate')], default='NA', max_length=2, verbose_name='Team scoring type'),
        ),
        migrations.AlterField(
            model_name='historicaleventtemplate',
            name='can_choose_hole',
            field=models.BooleanField(default=False, verbose_name='Member can choose starting hole'),
        ),
        migrations.AlterField(
            model_name='historicaleventtemplate',
            name='can_signup_group',
            field=models.BooleanField(default=False, verbose_name='Member can sign up group'),
        ),
        migrations.AlterField(
            model_name='historicaleventtemplate',
            name='description',
            field=models.TextField(verbose_name='Format and rules'),
        ),
        migrations.AlterField(
            model_name='historicaleventtemplate',
            name='event_fee',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Event fee'),
        ),
        migrations.AlterField(
            model_name='historicaleventtemplate',
            name='group_size',
            field=models.IntegerField(default=4, verbose_name='Group size'),
        ),
        migrations.AlterField(
            model_name='historicaleventtemplate',
            name='holes_per_round',
            field=models.IntegerField(default=18, verbose_name='Holes per round'),
        ),
        migrations.AlterField(
            model_name='historicaleventtemplate',
            name='maximum_signup_group_size',
            field=models.IntegerField(default=1, verbose_name='Maximum sign-up group size'),
        ),
        migrations.AlterField(
            model_name='historicaleventtemplate',
            name='minimum_signup_group_size',
            field=models.IntegerField(default=1, verbose_name='Minimum sign-up group size'),
        ),
        migrations.AlterField(
            model_name='historicaleventtemplate',
            name='name',
            field=models.CharField(db_index=True, max_length=100, verbose_name='Event title'),
        ),
        migrations.AlterField(
            model_name='historicaleventtemplate',
            name='number_of_scores',
            field=models.IntegerField(blank=True, default=1, verbose_name='Number of scores'),
        ),
        migrations.AlterField(
            model_name='historicaleventtemplate',
            name='rounds',
            field=models.IntegerField(default=1, verbose_name='Number of rounds'),
        ),
        migrations.AlterField(
            model_name='historicaleventtemplate',
            name='scoring',
            field=models.CharField(choices=[('IN', 'Individual'), ('T1', 'Team: One Score'), ('TM', 'Team: Multiple Scores')], default='IN', max_length=2, verbose_name='Scoring type'),
        ),
        migrations.AlterField(
            model_name='historicaleventtemplate',
            name='scoring_system',
            field=models.CharField(choices=[('SP', 'Stroke Play'), ('SF', 'Stableford'), ('CH', 'Chicago')], default='SP', max_length=2, verbose_name='Scoring system'),
        ),
        migrations.AlterField(
            model_name='historicaleventtemplate',
            name='skins_fee',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, verbose_name='Skins fee'),
        ),
        migrations.AlterField(
            model_name='historicaleventtemplate',
            name='team_scoring',
            field=models.CharField(choices=[('NA', 'Not a Team Event'), ('BB', 'Best Ball'), ('AGG', 'Aggregate')], default='NA', max_length=2, verbose_name='Team scoring type'),
        ),
    ]
