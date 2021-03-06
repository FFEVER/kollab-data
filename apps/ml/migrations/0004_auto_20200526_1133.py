# Generated by Django 3.0.5 on 2020-05-26 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ml', '0003_auto_20200526_1128'),
    ]

    operations = [
        migrations.RenameField(
            model_name='relation',
            old_name='projects_count',
            new_name='col_count',
        ),
        migrations.RenameField(
            model_name='relation',
            old_name='users_count',
            new_name='row_count',
        ),
        migrations.AddField(
            model_name='relation',
            name='col_type',
            field=models.CharField(default='Project', max_length=50),
        ),
        migrations.AddField(
            model_name='relation',
            name='row_type',
            field=models.CharField(default='User', max_length=50),
        ),
    ]
