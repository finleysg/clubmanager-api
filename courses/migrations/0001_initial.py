# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CourseSetup',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('holes', models.IntegerField(default=18)),
                ('slope', models.IntegerField()),
                ('rating', models.DecimalField(decimal_places=1, max_digits=4)),
                ('is_standard', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='CourseSetupHole',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('hole_number', models.IntegerField(default=0)),
                ('handicap', models.IntegerField()),
                ('course_setup', models.ForeignKey(to='courses.CourseSetup', on_delete=django.db.models.deletion.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='Hole',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('default_hole_number', models.IntegerField(default=0)),
                ('tee_name', models.CharField(max_length=12)),
                ('par', models.IntegerField(default=0)),
                ('default_handicap', models.IntegerField()),
                ('yardage', models.IntegerField()),
                ('course', models.ForeignKey(to='courses.Course', on_delete=django.db.models.deletion.CASCADE)),
            ],
        ),
        migrations.AddField(
            model_name='coursesetuphole',
            name='hole',
            field=models.ForeignKey(to='courses.Hole', on_delete=django.db.models.deletion.CASCADE),
        ),
    ]
