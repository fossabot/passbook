# Generated by Django 3.0.3 on 2020-02-20 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("passbook_sources_saml", "0004_auto_20200217_1526"),
    ]

    operations = [
        migrations.RenameField(
            model_name="samlsource", old_name="entity_id", new_name="issuer",
        ),
        migrations.AlterField(
            model_name="samlsource",
            name="issuer",
            field=models.TextField(
                blank=True,
                default=None,
                help_text="Also known as Entity ID. Defaults the Metadata URL.",
                verbose_name="Issuer",
            ),
        ),
    ]
