# Generated by Django 2.1.4 on 2018-12-11 00:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0007_auto_20171217_1558'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalannouncement',
            name='history_change_reason',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='historicalcontact',
            name='history_change_reason',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='announcement',
            name='document',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='documents.Document', verbose_name='Document'),
        ),
        migrations.AlterField(
            model_name='announcement',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='events.Event', verbose_name='Event'),
        ),
    ]
