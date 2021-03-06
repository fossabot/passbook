# Generated by Django 2.2.6 on 2019-11-07 13:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("passbook_core", "0005_merge_20191025_2022"),
    ]

    operations = [
        migrations.CreateModel(
            name="SAMLSource",
            fields=[
                (
                    "source_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="passbook_core.Source",
                    ),
                ),
                ("acs_url", models.URLField()),
                ("slo_url", models.URLField()),
                ("entity_id", models.TextField(blank=True, default=None)),
                ("idp_url", models.URLField()),
                ("auto_logout", models.BooleanField(default=False)),
                ("signing_cert", models.TextField()),
                ("signing_key", models.TextField()),
            ],
            options={"abstract": False,},
            bases=("passbook_core.source",),
        ),
    ]
