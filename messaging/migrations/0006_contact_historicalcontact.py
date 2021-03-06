# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-12-17 17:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('messaging', '0005_auto_20170109_1734'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('directors', models.TextField(verbose_name='Directors')),
                ('committees', models.TextField(verbose_name='Committees')),
                ('staff', models.TextField(verbose_name='Golf Course Staff')),
                ('president_name', models.CharField(max_length=100, verbose_name='Current President')),
                ('vice_president_name', models.CharField(max_length=100, verbose_name='Current Vice-President')),
                ('secretary_name', models.CharField(max_length=100, verbose_name='Current Secretary')),
                ('treasurer_name', models.CharField(max_length=100, verbose_name='Current Treasurer')),
                ('president_phone', models.CharField(max_length=20, verbose_name='President Phone')),
                ('vice_president_phone', models.CharField(max_length=20, verbose_name='Vice-President Phone')),
                ('secretary_phone', models.CharField(max_length=20, verbose_name='Secretary Phone')),
                ('treasurer_phone', models.CharField(max_length=20, verbose_name='Treasurer Phone')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalContact',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('directors', models.TextField(verbose_name='Directors')),
                ('committees', models.TextField(verbose_name='Committees')),
                ('staff', models.TextField(verbose_name='Golf Course Staff')),
                ('president_name', models.CharField(max_length=100, verbose_name='Current President')),
                ('vice_president_name', models.CharField(max_length=100, verbose_name='Current Vice-President')),
                ('secretary_name', models.CharField(max_length=100, verbose_name='Current Secretary')),
                ('treasurer_name', models.CharField(max_length=100, verbose_name='Current Treasurer')),
                ('president_phone', models.CharField(max_length=20, verbose_name='President Phone')),
                ('vice_president_phone', models.CharField(max_length=20, verbose_name='Vice-President Phone')),
                ('secretary_phone', models.CharField(max_length=20, verbose_name='Secretary Phone')),
                ('treasurer_phone', models.CharField(max_length=20, verbose_name='Treasurer Phone')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical contact',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
    ]
