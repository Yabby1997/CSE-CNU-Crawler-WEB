from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	portal_id = models.CharField(max_length=50)
	portal_pw = models.CharField(max_length=50)
	last_update = models.DateTimeField(default=timezone.now)
	
'''
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
'''
