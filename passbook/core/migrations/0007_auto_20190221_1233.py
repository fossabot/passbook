# Generated by Django 2.1.7 on 2019-02-21 12:33

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('passbook_core', '0006_factor_arguments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factor',
            name='arguments',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict),
        ),
    ]