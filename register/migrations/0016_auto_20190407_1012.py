# Generated by Django 2.1.7 on 2019-04-07 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0015_auto_20181215_0953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalregistrationgroup',
            name='course_setup',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='courses.CourseSetup', verbose_name='Course'),
        ),
        migrations.AlterField(
            model_name='historicalregistrationgroup',
            name='event',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='events.Event', verbose_name='Event'),
        ),
        migrations.AlterField(
            model_name='historicalregistrationgroup',
            name='signed_up_by',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.Member', verbose_name='Signed up by'),
        ),
        migrations.AlterField(
            model_name='historicalregistrationrefund',
            name='recorded_by',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.Member', verbose_name='Recorded by'),
        ),
        migrations.AlterField(
            model_name='historicalregistrationslot',
            name='course_setup_hole',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='courses.CourseSetupHole', verbose_name='Hole'),
        ),
        migrations.AlterField(
            model_name='historicalregistrationslot',
            name='event',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='events.Event', verbose_name='Event'),
        ),
        migrations.AlterField(
            model_name='historicalregistrationslot',
            name='member',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.Member', verbose_name='Member'),
        ),
        migrations.AlterField(
            model_name='historicalregistrationslot',
            name='registration_group',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='register.RegistrationGroup', verbose_name='Group'),
        ),
        migrations.AlterField(
            model_name='historicalregistrationslotpayment',
            name='recorded_by',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.Member', verbose_name='Member'),
        ),
        migrations.AlterField(
            model_name='historicalregistrationslotpayment',
            name='registration_slot',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='register.RegistrationSlot', verbose_name='Registration'),
        ),
        migrations.AlterField(
            model_name='registrationslot',
            name='course_setup_hole',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='courses.CourseSetupHole', verbose_name='Hole'),
        ),
        migrations.AlterField(
            model_name='registrationslotpayment',
            name='registration_slot',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payments', to='register.RegistrationSlot', verbose_name='Registration'),
        ),
    ]