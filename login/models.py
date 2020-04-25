from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	#account_id = models.IntegerField()
	#portal_id = models.CharField(max_length=30)
	#portal_pw = models.CharField(max_length=30)
	#last_login = models.DateTimeField()
	
	def __str__(self):
		return self.user


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
