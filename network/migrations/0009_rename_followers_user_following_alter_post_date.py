# Generated by Django 4.0 on 2022-02-06 03:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0008_alter_post_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='followers',
            new_name='following',
        ),
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 5, 22, 0, 44, 398226, tzinfo=utc)),
        ),
    ]
