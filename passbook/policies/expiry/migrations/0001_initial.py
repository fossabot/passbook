# Generated by Django 2.2.6 on 2019-10-07 14:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("passbook_core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PasswordExpiryPolicy",
            fields=[
                (
                    "policy_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="passbook_core.Policy",
                    ),
                ),
                ("deny_only", models.BooleanField(default=False)),
                ("days", models.IntegerField()),
            ],
            options={
                "verbose_name": "Password Expiry Policy",
                "verbose_name_plural": "Password Expiry Policies",
            },
            bases=("passbook_core.policy",),
        ),
    ]
