# Generated by Django 4.0.2 on 2022-04-24 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studyapp', '0002_course_course_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_title',
            field=models.CharField(default='', max_length=300),
        ),
    ]