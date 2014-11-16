from django.db import models

# Create your models here.

class SwagType(models.Model):
	id = models.IntegerField(primary_key = True)
	name = models.CharField(max_length = 200)
	orderable = models.CharField(max_length = 10)
	amount = models.IntegerField()

	def __unicode__(self):
		return self.name
