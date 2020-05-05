from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.validators import RegexValidator


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    portal_id = models.CharField(max_length=9, validators=[RegexValidator('^[0-9]*$')])
    portal_pw = models.CharField(max_length=300)
    last_update = models.DateTimeField(default=timezone.now)
