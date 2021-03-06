# Generated by Django 3.0.3 on 2020-02-22 18:22

from django.db import migrations


def fix_application_null(apps, schema_editor):
    """Fix Application meta_fields being null"""
    Application = apps.get_model("passbook_core", "Application")
    for app in Application.objects.all():
        if app.meta_launch_url is None:
            app.meta_launch_url = ""
        if app.meta_icon_url is None:
            app.meta_icon_url = ""
        if app.meta_description is None:
            app.meta_description = ""
        if app.meta_publisher is None:
            app.meta_publisher = ""
        app.save()


class Migration(migrations.Migration):

    dependencies = [
        ("passbook_core", "0010_auto_20200221_2208"),
    ]

    operations = [migrations.RunPython(fix_application_null)]
