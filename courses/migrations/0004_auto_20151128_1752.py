# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_auto_20151106_1953'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coursesetup',
            old_name='holes',
            new_name='number_of_holes',
        ),
        migrations.RenameField(
            model_name='historicalcoursesetup',
            old_name='holes',
            new_name='number_of_holes',
        ),
    ]
