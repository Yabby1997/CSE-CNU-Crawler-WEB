from django.db import models


class NoticeData(models.Model):
	link = models.TextField()
	type = models.TextField()
	date = models.TextField()
	title = models.TextField()
	number = models.TextField(null=True)

	def __str__(self):
		return self.title
