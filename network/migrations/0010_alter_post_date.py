# Generated by Django 4.0 on 2022-02-06 03:01

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0009_rename_followers_user_following_alter_post_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 5, 22, 1, 42, 977182, tzinfo=utc)),
        ),
    ]