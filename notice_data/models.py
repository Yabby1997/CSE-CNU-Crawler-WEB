from django.db import models


class NoticeData(models.Model):
	link = models.TextField()
	title = models.TextField()
	text = models.TextField()

	def __str__(self):
		return self.title