# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('description', models.CharField(max_length=200)),
                ('address1', models.CharField(max_length=100)),
                ('address2', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=40)),
                ('state', models.CharField(max_length=20)),
                ('zip', models.CharField(max_length=10)),
                ('website', models.CharField(max_length=300)),
                ('contact_email', models.CharField(max_length=300)),
                ('phone_number', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalClub',
            fields=[
                ('id', models.IntegerField(blank=True, auto_created=True, db_index=True, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('address1', models.CharField(max_length=100)),
                ('address2', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=40)),
                ('state', models.CharField(max_length=20)),
                ('zip', models.CharField(max_length=10)),
                ('website', models.CharField(max_length=300)),
                ('contact_email', models.CharField(max_length=300)),
                ('phone_number', models.CharField(max_length=20)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True, related_name='+')),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical club',
            },
        ),
        migrations.CreateModel(
            name='HistoricalMember',
            fields=[
                ('id', models.IntegerField(blank=True, auto_created=True, db_index=True, verbose_name='ID')),
                ('address1', models.CharField(max_length=100)),
                ('address2', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=40)),
                ('state', models.CharField(max_length=20)),
                ('zip', models.CharField(max_length=10)),
                ('phone_number', models.CharField(max_length=20)),
                ('ghin', models.CharField(max_length=7)),
                ('handicap', models.DecimalField(max_digits=3, decimal_places=1)),
                ('handicap_revision_date', models.DateField()),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True, related_name='+')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, to=settings.AUTH_USER_MODEL, related_name='+', null=True, blank=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical member',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('address1', models.CharField(max_length=100)),
                ('address2', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=40)),
                ('state', models.CharField(max_length=20)),
                ('zip', models.CharField(max_length=10)),
                ('phone_number', models.CharField(max_length=20)),
                ('ghin', models.CharField(max_length=7)),
                ('handicap', models.DecimalField(max_digits=3, decimal_places=1)),
                ('handicap_revision_date', models.DateField()),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
