# Generated by Django 4.0.2 on 2022-04-18 18:39

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('studyapp', '0004_alter_meeting_post_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='post_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 18, 18, 39, 52, 675697, tzinfo=utc), verbose_name='date posted'),
        ),
    ]
