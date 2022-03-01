import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

class Meeting(models.Model):
    post_text = models.CharField(max_length=200)
    post_date = models.DateTimeField('date posted')
    def __str__(self):
        return self.post_text
    def was_posted_recently(self):
        return self.post_date >= timezone.now() - datetime.timedelta(days=1)


class Reply(models.Model):
    post = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

