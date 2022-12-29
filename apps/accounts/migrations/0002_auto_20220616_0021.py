# Generated by Django 3.2.14 on 2022-12-28 10:39

import common.db.encoder
import common.db.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ('assets', '0106_auto_20221228_1838'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountBackupAutomation',
            fields=[
                ('created_by', models.CharField(blank=True, max_length=128, null=True, verbose_name='Created by')),
                ('updated_by', models.CharField(blank=True, max_length=128, null=True, verbose_name='Updated by')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date updated')),
                ('comment', models.TextField(blank=True, default='', verbose_name='Comment')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('org_id',
                 models.CharField(blank=True, db_index=True, default='', max_length=36, verbose_name='Organization')),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('is_periodic', models.BooleanField(default=False, verbose_name='Periodic perform')),
                ('interval', models.IntegerField(blank=True, default=24, null=True, verbose_name='Cycle perform')),
                ('crontab', models.CharField(blank=True, max_length=128, null=True, verbose_name='Regularly perform')),
                ('types', models.JSONField(default=list)),
                ('recipients', models.ManyToManyField(blank=True, related_name='recipient_escape_route_plans',
                                                      to=settings.AUTH_USER_MODEL, verbose_name='Recipient')),
            ],
            options={
                'verbose_name': 'Account backup plan',
                'ordering': ['name'],
                'unique_together': {('name', 'org_id')},
            },
        ),
        migrations.CreateModel(
            name='AccountBaseAutomation',
            fields=[
                ('created_by', models.CharField(blank=True, max_length=128, null=True, verbose_name='Created by')),
                ('updated_by', models.CharField(blank=True, max_length=128, null=True, verbose_name='Updated by')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date updated')),
                ('comment', models.TextField(blank=True, default='', verbose_name='Comment')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('org_id',
                 models.CharField(blank=True, db_index=True, default='', max_length=36, verbose_name='Organization')),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('is_periodic', models.BooleanField(default=False, verbose_name='Periodic perform')),
                ('interval', models.IntegerField(blank=True, default=24, null=True, verbose_name='Cycle perform')),
                ('crontab', models.CharField(blank=True, max_length=128, null=True, verbose_name='Regularly perform')),
                ('type', models.CharField(max_length=16, verbose_name='Type')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('accounts', models.JSONField(default=list, verbose_name='Accounts')),
                ('assets', models.ManyToManyField(blank=True, to='assets.Asset', verbose_name='Assets')),
                ('nodes', models.ManyToManyField(blank=True, to='assets.Node', verbose_name='Nodes')),
            ],
            options={
                'verbose_name': 'Automation task',
                'abstract': False,
                'unique_together': {('org_id', 'name')},
            },
        ),
        migrations.CreateModel(
            name='AutomationExecution',
            fields=[
            ],
            options={
                'verbose_name': 'Automation execution',
                'verbose_name_plural': 'Automation executions',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('assets.automationexecution',),
        ),
        migrations.CreateModel(
            name='GatherAccountsAutomation',
            fields=[
                ('accountbaseautomation_ptr',
                 models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True,
                                      primary_key=True, serialize=False, to='accounts.accountbaseautomation')),
            ],
            options={
                'verbose_name': 'Gather asset accounts',
            },
            bases=('accounts.accountbaseautomation',),
        ),
        migrations.CreateModel(
            name='PushAccountAutomation',
            fields=[
                ('accountbaseautomation_ptr',
                 models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True,
                                      primary_key=True, serialize=False, to='accounts.accountbaseautomation')),
                ('secret_type', models.CharField(
                    choices=[('password', 'Password'), ('ssh_key', 'SSH key'), ('access_key', 'Access key'),
                             ('token', 'Token')], default='password', max_length=16, verbose_name='Secret type')),
                ('secret_strategy', models.CharField(choices=[('specific', 'Specific password'),
                                                              ('random_one', 'All assets use the same random password'),
                                                              ('random_all',
                                                               'All assets use different random password')],
                                                     default='specific', max_length=16,
                                                     verbose_name='Secret strategy')),
                ('secret', common.db.fields.EncryptTextField(blank=True, null=True, verbose_name='Secret')),
                ('password_rules', models.JSONField(default=dict, verbose_name='Password rules')),
                ('ssh_key_change_strategy', models.CharField(
                    choices=[('add', 'Append SSH KEY'), ('set', 'Empty and append SSH KEY'),
                             ('set_jms', 'Replace (The key generated by JumpServer) ')], default='add', max_length=16,
                    verbose_name='SSH key change strategy')),
                ('username', models.CharField(max_length=128, verbose_name='Username')),
            ],
            options={
                'verbose_name': 'Push asset account',
            },
            bases=('accounts.accountbaseautomation', models.Model),
        ),
        migrations.CreateModel(
            name='VerifyAccountAutomation',
            fields=[
                ('accountbaseautomation_ptr',
                 models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True,
                                      primary_key=True, serialize=False, to='accounts.accountbaseautomation')),
            ],
            options={
                'verbose_name': 'Verify asset account',
            },
            bases=('accounts.accountbaseautomation',),
        ),
        migrations.CreateModel(
            name='ChangeSecretRecord',
            fields=[
                ('created_by', models.CharField(blank=True, max_length=128, null=True, verbose_name='Created by')),
                ('updated_by', models.CharField(blank=True, max_length=128, null=True, verbose_name='Updated by')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date updated')),
                ('comment', models.TextField(blank=True, default='', verbose_name='Comment')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('old_secret', common.db.fields.EncryptTextField(blank=True, null=True, verbose_name='Old secret')),
                ('new_secret', common.db.fields.EncryptTextField(blank=True, null=True, verbose_name='Secret')),
                ('date_started', models.DateTimeField(blank=True, null=True, verbose_name='Date started')),
                ('date_finished', models.DateTimeField(blank=True, null=True, verbose_name='Date finished')),
                ('status', models.CharField(default='pending', max_length=16)),
                ('error', models.TextField(blank=True, null=True, verbose_name='Error')),
                ('account',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.account')),
                ('asset', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.asset')),
                ('execution',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.automationexecution')),
            ],
            options={
                'verbose_name': 'Change secret record',
            },
        ),
        migrations.CreateModel(
            name='AccountBackupExecution',
            fields=[
                ('org_id',
                 models.CharField(blank=True, db_index=True, default='', max_length=36, verbose_name='Organization')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('date_start', models.DateTimeField(auto_now_add=True, verbose_name='Date start')),
                ('timedelta', models.FloatField(default=0.0, null=True, verbose_name='Time')),
                ('plan_snapshot',
                 models.JSONField(blank=True, default=dict, encoder=common.db.encoder.ModelJSONFieldEncoder, null=True,
                                  verbose_name='Account backup snapshot')),
                ('trigger', models.CharField(choices=[('manual', 'Manual trigger'), ('timing', 'Timing trigger')],
                                             default='manual', max_length=128, verbose_name='Trigger mode')),
                ('reason', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Reason')),
                ('is_success', models.BooleanField(default=False, verbose_name='Is success')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='execution',
                                           to='accounts.accountbackupautomation', verbose_name='Account backup plan')),
            ],
            options={
                'verbose_name': 'Account backup execution',
            },
        ),
        migrations.CreateModel(
            name='ChangeSecretAutomation',
            fields=[
                ('accountbaseautomation_ptr',
                 models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True,
                                      primary_key=True, serialize=False, to='accounts.accountbaseautomation')),
                ('secret_type', models.CharField(
                    choices=[('password', 'Password'), ('ssh_key', 'SSH key'), ('access_key', 'Access key'),
                             ('token', 'Token')], default='password', max_length=16, verbose_name='Secret type')),
                ('secret_strategy', models.CharField(
                    choices=[('specific', 'Specific password'),
                             ('random_one', 'All assets use the same random password'),
                             ('random_all', 'All assets use different random password')], default='specific',
                    max_length=16, verbose_name='Secret strategy')),
                ('secret', common.db.fields.EncryptTextField(blank=True, null=True, verbose_name='Secret')),
                ('password_rules', models.JSONField(default=dict, verbose_name='Password rules')),
                ('ssh_key_change_strategy', models.CharField(
                    choices=[('add', 'Append SSH KEY'), ('set', 'Empty and append SSH KEY'),
                             ('set_jms', 'Replace (The key generated by JumpServer) ')], default='add', max_length=16,
                    verbose_name='SSH key change strategy')),
                ('recipients',
                 models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Recipient')),
            ],
            options={
                'verbose_name': 'Change secret automation',
            },
            bases=('accounts.accountbaseautomation', models.Model),
        ),
    ]