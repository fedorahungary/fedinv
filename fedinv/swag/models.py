from django.db import models
from django.template.defaulttags import register
import json

class SwagType(models.Model):
	id = models.IntegerField(primary_key = True)
	name = models.CharField(max_length = 200)
	orderable = models.CharField(max_length = 10)
	amount = models.IntegerField()

	def __unicode__(self):
		return self.name

@register.filter
def swag_id_to_name(sid):
	s = SwagType.objects.all()
	_sid = int(sid)
	for _s in s:
		if (_s.id == _sid):
			return _s.name
	return "NULL"

class Person(models.Model):
	id = models.IntegerField(primary_key = True)
	name = models.CharField(max_length=5000)
	team = models.IntegerField()
	# serialized with JSON
	held_swag = models.CharField(max_length=5000)

	@property
	def d_held_swag(self):
		return self.get_swag(self)

	def get_swag(self):
		return json.loads(self.held_swag)
	
	def set_swag(self, d_held):
		held_swag = json.dumps(d_held)

	def __unicode__(self):
		return self.name
