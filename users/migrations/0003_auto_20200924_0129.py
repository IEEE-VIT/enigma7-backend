# Generated by Django 3.0.8 on 2020-09-23 19:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200921_2242'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userstatus',
            old_name='point_timestamp',
            new_name='last_answered_ts',
        ),
    ]
