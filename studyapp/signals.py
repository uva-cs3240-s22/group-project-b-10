from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User, dispatch_uid='user.create_user_profile')
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, name = user.first + " " + user.last)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()