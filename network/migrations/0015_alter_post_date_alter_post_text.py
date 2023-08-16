# Generated by Django 4.0 on 2022-02-17 02:36

import datetime
import django.core.validators
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0014_rename_likes_post_likers_alter_post_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 16, 21, 36, 11, 200036, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.CharField(max_length=1000, validators=[django.core.validators.MinLengthValidator(4)]),
        ),
    ]
