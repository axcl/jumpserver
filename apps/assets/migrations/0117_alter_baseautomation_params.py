# Generated by Django 3.2.17 on 2023-05-06 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0116_auto_20230418_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseautomation',
            name='params',
            field=models.JSONField(default=dict, verbose_name='Parameters'),
        ),
    ]
