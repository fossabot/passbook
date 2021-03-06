# Generated by Django 3.0.3 on 2020-02-17 16:15

from django.db import migrations


def cleanup_old_autogenerated(apps, schema_editor):
    SAMLPropertyMapping = apps.get_model(
        "passbook_providers_saml", "SAMLPropertyMapping"
    )
    db_alias = schema_editor.connection.alias
    SAMLPropertyMapping.objects.using(db_alias).filter(
        name__startswith="Autogenerated"
    ).delete()


def create_default_property_mappings(apps, schema_editor):
    """Create default SAML Property Mappings"""
    SAMLPropertyMapping = apps.get_model(
        "passbook_providers_saml", "SAMLPropertyMapping"
    )
    db_alias = schema_editor.connection.alias
    defaults = [
        {
            "FriendlyName": "eduPersonPrincipalName",
            "Name": "urn:oid:1.3.6.1.4.1.5923.1.1.1.6",
            "Expression": "{{ user.email }}",
        },
        {
            "FriendlyName": "cn",
            "Name": "urn:oid:2.5.4.3",
            "Expression": "{{ user.name }}",
        },
        {
            "FriendlyName": "mail",
            "Name": "urn:oid:0.9.2342.19200300.100.1.3",
            "Expression": "{{ user.email }}",
        },
        {
            "FriendlyName": "displayName",
            "Name": "urn:oid:2.16.840.1.113730.3.1.241",
            "Expression": "{{ user.username }}",
        },
        {
            "FriendlyName": "uid",
            "Name": "urn:oid:0.9.2342.19200300.100.1.1",
            "Expression": "{{ user.pk }}",
        },
        {
            "FriendlyName": "member-of",
            "Name": "member-of",
            "Expression": "[{% for group in user.groups.all() %}'{{ group.name }}',{% endfor %}]",
        },
    ]
    for default in defaults:
        SAMLPropertyMapping.objects.using(db_alias).get_or_create(
            saml_name=default["Name"],
            friendly_name=default["FriendlyName"],
            expression=default["Expression"],
            defaults={
                "name": f"Autogenerated SAML Mapping: {default['FriendlyName']} -> {default['Expression']}"
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ("passbook_providers_saml", "0004_auto_20200217_1526"),
        ("passbook_core", "0007_auto_20200217_1934"),
    ]

    operations = [
        migrations.RunPython(cleanup_old_autogenerated),
        migrations.RemoveField(model_name="samlpropertymapping", name="values",),
        migrations.RunPython(create_default_property_mappings),
    ]
