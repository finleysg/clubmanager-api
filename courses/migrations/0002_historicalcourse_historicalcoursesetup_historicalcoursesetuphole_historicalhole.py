# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalCourse',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', blank=True, db_index=True, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL)),
            ],
            options={
                'verbose_name': 'historical course',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalCourseSetup',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', blank=True, db_index=True, auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('holes', models.IntegerField(default=18)),
                ('slope', models.IntegerField()),
                ('rating', models.DecimalField(decimal_places=1, max_digits=4)),
                ('is_standard', models.BooleanField(default=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL)),
            ],
            options={
                'verbose_name': 'historical course setup',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalCourseSetupHole',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', blank=True, db_index=True, auto_created=True)),
                ('hole_number', models.IntegerField(default=0)),
                ('handicap', models.IntegerField()),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('course_setup', models.ForeignKey(blank=True, db_constraint=False, to='courses.CourseSetup', null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING)),
                ('history_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL)),
                ('hole', models.ForeignKey(blank=True, db_constraint=False, to='courses.Hole', null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING)),
            ],
            options={
                'verbose_name': 'historical course setup hole',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalHole',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', blank=True, db_index=True, auto_created=True)),
                ('default_hole_number', models.IntegerField(default=0)),
                ('tee_name', models.CharField(max_length=12)),
                ('par', models.IntegerField(default=0)),
                ('default_handicap', models.IntegerField()),
                ('yardage', models.IntegerField()),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('course', models.ForeignKey(blank=True, db_constraint=False, to='courses.Course', null=True, related_name='+', on_delete=django.db.models.deletion.DO_NOTHING)),
                ('history_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL)),
            ],
            options={
                'verbose_name': 'historical hole',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
    ]
