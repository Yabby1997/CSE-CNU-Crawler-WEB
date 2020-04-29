from django.db import models
from login.models import Profile


class ElearnData(models.Model):
    userID = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.TextField()
    percentage = models.TextField()
    video0 = models.IntegerField()
    video1 = models.IntegerField()
    video2 = models.IntegerField()
    video3 = models.IntegerField()
    video4 = models.IntegerField()
    report0 = models.IntegerField()
    report1 = models.IntegerField()
    videos2watch = models.TextField(default="")
    reports2do = models.TextField(default="")

    def __str__(self):
        return self.title
