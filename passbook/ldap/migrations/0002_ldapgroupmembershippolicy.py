# Generated by Django 2.1.7 on 2019-03-10 18:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passbook_core', '0020_groupmembershippolicy'),
        ('passbook_ldap', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LDAPGroupMembershipPolicy',
            fields=[
                ('policy_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='passbook_core.Policy')),
                ('dn', models.TextField()),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='passbook_ldap.LDAPSource')),
            ],
            options={
                'verbose_name': 'LDAP Group Membership Policy',
                'verbose_name_plural': 'LDAP Group Membership Policys',
            },
            bases=('passbook_core.policy',),
        ),
    ]