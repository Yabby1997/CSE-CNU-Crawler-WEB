from django.db import models
from login.models import Profile


class ElearnData(models.Model):
    userID = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.TextField()
    percentage = models.TextField()
    videos = models.TextField(default="")
    reports = models.TextField(default="")
    videosDetail = models.TextField(default="")
    reportsDetail = models.TextField(default="")
    notices = models.TextField(default="")
    materials = models.TextField(default="")
    
    def __str__(self):
        return self.title
