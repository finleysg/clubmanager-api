# Generated by Django 2.1.7 on 2019-04-05 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0008_auto_20181210_1836'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='display_flag',
            field=models.BooleanField(default=False, verbose_name='Show on the Website'),
        ),
        migrations.AddField(
            model_name='historicaldocument',
            name='display_flag',
            field=models.BooleanField(default=False, verbose_name='Show on the Website'),
        ),
        migrations.AlterField(
            model_name='historicaldocument',
            name='event',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='events.Event', verbose_name='Event'),
        ),
        migrations.AlterField(
            model_name='historicalphoto',
            name='event',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='events.Event', verbose_name='Event'),
        ),
    ]
