import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

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

class Reply(models.Model):
    post = models.ForeignKey('Meeting', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

class Profile(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = models.Manager()
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    friends = models.ManyToManyField("Profile")
    enrolled_courses = models.CharField(max_length=200)  # Eventually should be array
    selected_courses = models.CharField(max_length=200)  # Eventually should be array
    # a user's/profile's relationship to meetings is many to many.
    # A meeting might have many profiles
    # A profile might have many meetings
    meetings = models.ManyToManyField('Meeting')


    def __str__(self):
        return f'{self.user.username} Profile'

class Friend_Request(models.Model):
    from_user = models.ForeignKey(Profile, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(Profile, related_name='to_user', on_delete=models.CASCADE)

class Room(models.Model):
    """Represents chat rooms that users can join"""
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    slug = models.CharField(max_length=50)

    def __str__(self):
        """Returns human-readable representation of the model instance."""
        return self.name
class Meeting(models.Model):
    # should meeting have a course associated with it?
    # course is a many to one relationship so we use models.ForeignKey()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=None)
    # we want location data
    # for now address
    location = models.CharField(max_length=400, default=None)
    # person who created meeting
    buddies = models.ManyToManyField(Profile)
    # partners = models.ForeignKey(Profile, on_delete=models.CASCADE, default = None)
    # we want time
    start_time = post_date = models.DateTimeField('Start time', default=None)
    end_time = models.DateTimeField('End time', default=None)

    post_text = models.CharField(max_length=200)
    post_date = models.DateTimeField('date posted', default=timezone.now)
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
