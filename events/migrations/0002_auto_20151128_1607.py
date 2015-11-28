# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='holes',
            new_name='holes_per_round',
        ),
        migrations.RenameField(
            model_name='eventtemplate',
            old_name='holes',
            new_name='holes_per_round',
        ),
        migrations.RenameField(
            model_name='historicalevent',
            old_name='holes',
            new_name='holes_per_round',
        ),
        migrations.RenameField(
            model_name='historicaleventtemplate',
            old_name='holes',
            new_name='holes_per_round',
        ),
        migrations.AlterField(
            model_name='event',
            name='number_of_scores',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='eventtemplate',
            name='number_of_scores',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='historicalevent',
            name='number_of_scores',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='historicaleventtemplate',
            name='number_of_scores',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
