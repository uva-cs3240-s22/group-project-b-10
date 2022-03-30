import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin

# Create your models here.
class Course(models.Model):
#     field: name, id, etc
    objects = models.Manager()
    course_name = models.CharField(max_length=200)
    department = models.CharField(max_length=200, default="DEP")
    # course_id = models.CharField(max_length=50)
    # @admin.display(
    #     boolean=True,
    #     ordering='course_name'
    # )
    def __str__(self):
        return self.course_name

class Meeting(models.Model):
    post_text = models.CharField(max_length=200)
    post_date = models.DateTimeField('date posted')
    def __str__(self):
        return self.post_text
    @admin.display(
        boolean=True,
        ordering='post_date',
        description='Posted recently?',
    )
    def was_posted_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.post_date <= now


class Reply(models.Model):
    post = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
