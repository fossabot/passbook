# Generated by Django 2.1.4 on 2018-12-10 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passbook_core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fieldmatcherrule',
            name='user_field',
            field=models.TextField(choices=[('username', 'username'), ('first_name', 'first_name'), ('last_name', 'last_name'), ('email', 'email'), ('is_staff', 'is_staff'), ('is_active', 'is_active'), ('data_joined', 'data_joined')]),
        ),
    ]