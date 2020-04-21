from django.db import models


class NoticeData(models.Model):
	link = models.TextField()
	type = models.TextField()
	date = models.TextField()
	title = models.TextField()
	text = models.TextField()

	def __str__(self):
		return self.title