from django.db import models

class Report(models.Model):
	id = models.IntegerField(primary_key = True)
	name = models.CharField(max_length = 200)
	url = models.CharField(max_length = 10)
	
	def __unicode__(self):
		return self.url

