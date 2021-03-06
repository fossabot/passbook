# Generated by Django 2.2.6 on 2019-10-07 14:11

from django.db import migrations


def create_initial_factor(apps, schema_editor):
    """Create initial PasswordFactor if none exists"""
    PasswordFactor = apps.get_model("passbook_factors_password", "PasswordFactor")
    if not PasswordFactor.objects.exists():
        PasswordFactor.objects.create(
            name="password",
            slug="password",
            order=0,
            backends=["django.contrib.auth.backends.ModelBackend"],
        )


class Migration(migrations.Migration):

    dependencies = [
        ("passbook_factors_password", "0001_initial"),
    ]

    operations = [migrations.RunPython(create_initial_factor)]
