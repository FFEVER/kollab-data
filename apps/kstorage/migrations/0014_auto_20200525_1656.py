# Generated by Django 3.0.5 on 2020-05-25 16:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kstorage', '0013_auto_20200525_1138'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='categories',
            new_name='fields',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='expertises',
            new_name='fields',
        ),
    ]
