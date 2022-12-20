# Generated by Django 3.2.12 on 2022-07-11 06:13

import time
from django.db import migrations
from assets.models import Platform


def migrate_accounts(apps, schema_editor):
    auth_book_model = apps.get_model('assets', 'AuthBook')
    account_model = apps.get_model('assets', 'Account')

    count = 0
    bulk_size = 1000
    print("\n\tStart migrate accounts")
    while True:
        start = time.time()
        auth_books = auth_book_model.objects \
            .prefetch_related('systemuser') \
            .all()[count:count+bulk_size]
        if not auth_books:
            break

        count += len(auth_books)
        accounts = []
        # auth book 和 account 相同的属性
        same_attrs = [
            'id', 'username', 'comment', 'date_created', 'date_updated',
            'created_by', 'asset_id', 'org_id',
        ]
        # 认证的属性，可能是 authbook 的，可能是 systemuser 的
        auth_attrs = ['password', 'private_key', 'token']
        all_attrs = same_attrs + auth_attrs

        for auth_book in auth_books:
            values = {'version': 1}

            system_user = auth_book.systemuser
            if system_user:
                # 更新一次系统用户的认证属性
                values.update({attr: getattr(system_user, attr, '') for attr in all_attrs})
                values['created_by'] = str(system_user.id)
                values['privileged'] = system_user.type == 'admin'

            auth_book_auth = {attr: getattr(auth_book, attr, '') for attr in all_attrs if getattr(auth_book, attr, '')}
            # 最终使用 authbook 的认证属性
            values.update(auth_book_auth)

            auth_infos = []
            username = values['username']
            for attr in auth_attrs:
                secret = values.pop(attr, None)
                if not secret:
                    continue

                if attr == 'private_key':
                    secret_type = 'ssh_key'
                    name = f'{username}(ssh key)'
                elif attr == 'token':
                    secret_type = 'token'
                    name = f'{username}(token)'
                else:
                    secret_type = attr
                    name = username
                auth_infos.append((name, secret_type, secret))

            if not auth_infos:
                auth_infos.append((username, 'password', ''))

            for name, secret_type, secret in auth_infos:
                account = account_model(**values, name=name, secret=secret, secret_type=secret_type)
                accounts.append(account)

        account_model.objects.bulk_create(accounts, ignore_conflicts=True)
        print("\t  - Create accounts: {}-{} using: {:.2f}s".format(
            count - len(auth_books), count, time.time()-start
        ))


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0099_auto_20220711_1409'),
    ]

    operations = [
        migrations.RunPython(migrate_accounts),
    ]