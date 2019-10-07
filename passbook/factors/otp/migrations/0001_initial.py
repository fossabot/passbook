# Generated by Django 2.2.6 on 2019-10-07 14:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('passbook_core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OTPFactor',
            fields=[
                ('factor_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='passbook_core.Factor')),
                ('enforced', models.BooleanField(default=False, help_text='Enforce enabled OTP for Users this factor applies to.')),
            ],
            options={
                'verbose_name': 'OTP Factor',
                'verbose_name_plural': 'OTP Factors',
            },
            bases=('passbook_core.factor',),
        ),
    ]