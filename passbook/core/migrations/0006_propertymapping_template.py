# Generated by Django 3.0.3 on 2020-02-17 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("passbook_core", "0005_merge_20191025_2022"),
    ]

    operations = [
        migrations.AddField(
            model_name="propertymapping",
            name="template",
            field=models.TextField(default=""),
            preserve_default=False,
        ),
    ]
