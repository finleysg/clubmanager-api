# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2018-03-04 00:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0018_auto_20171226_1439'),
        ('register', '0012_auto_20170911_1825'),
    ]

    operations = [
        migrations.CreateModel(
            name='OnlinePayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.IntegerField(verbose_name='Event Id')),
                ('name', models.CharField(max_length=100, verbose_name='Event Name')),
                ('event_type', models.CharField(max_length=1, verbose_name='Event Type')),
                ('start_date', models.DateField(verbose_name='Start date')),
                ('signed_up_by_id', models.IntegerField(verbose_name='Member Id')),
                ('first_name', models.CharField(max_length=40, verbose_name='Member First Name')),
                ('last_name', models.CharField(max_length=60, verbose_name='Member Last Name')),
                ('payment_confirmation_code', models.CharField(max_length=30, verbose_name='Payment confirmation code')),
                ('payment_confirmation_timestamp', models.DateTimeField(verbose_name='Payment confirmation timestamp')),
                ('payment_amount', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Payment amount')),
                ('record_id', models.IntegerField(verbose_name='Record Id')),
                ('record_type', models.CharField(max_length=12, verbose_name='Record Type')),
                ('pkey', models.CharField(max_length=10, verbose_name='Key')),
            ],
            options={
                'verbose_name_plural': 'Online Payments',
                'db_table': 'online_payment_view',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='HistoricalRegistrationRefund',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('related_record_id', models.IntegerField(verbose_name='Related record id')),
                ('related_record_name', models.CharField(max_length=30, verbose_name='Related record name')),
                ('refund_code', models.CharField(max_length=30, verbose_name='Refund code')),
                ('refund_timestamp', models.DateTimeField(blank=True, editable=False, verbose_name='Refund timestamp')),
                ('refund_amount', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Refund amount')),
                ('comment', models.CharField(blank=True, max_length=200, verbose_name='Comment')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('recorded_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.Member')),
            ],
            options={
                'verbose_name': 'historical registration refund',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='RegistrationRefund',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('related_record_id', models.IntegerField(verbose_name='Related record id')),
                ('related_record_name', models.CharField(max_length=30, verbose_name='Related record name')),
                ('refund_code', models.CharField(max_length=30, verbose_name='Refund code')),
                ('refund_timestamp', models.DateTimeField(auto_now=True, verbose_name='Refund timestamp')),
                ('refund_amount', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Refund amount')),
                ('comment', models.CharField(blank=True, max_length=200, verbose_name='Comment')),
                ('recorded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Member', verbose_name='Recorded by')),
            ],
        ),
    ]
