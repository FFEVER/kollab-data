# Generated by Django 3.0.5 on 2020-05-25 11:38

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kstorage', '0012_auto_20200518_1832'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='followed_projects',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True, null=True), default=list, size=None),
        ),
        migrations.AddField(
            model_name='user',
            name='joined_projects',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True, null=True), default=list, size=None),
        ),
        migrations.AddField(
            model_name='user',
            name='starred_projects',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True, null=True), default=list, size=None),
        ),
        migrations.AddField(
            model_name='user',
            name='viewed_projects',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True, null=True), default=list, size=None),
        ),
    ]
