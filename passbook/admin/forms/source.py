"""passbook core source form fields"""
# from django import forms

SOURCE_FORM_FIELDS = ["name", "slug", "enabled", "policies"]
SOURCE_SERIALIZER_FIELDS = ["pk", "name", "slug", "enabled", "policies"]

# class SourceForm(forms.Form)