from django.db import models
from django.template.defaulttags import register
from django.core.mail import send_mail
from fedinv import settings
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

class Order(models.Model):
	from_id = models.IntegerField()
	to_id = models.IntegerField()
	swag_id = models.IntegerField()
	amount = models.IntegerField()
	error_reason = models.CharField(max_length=500)

	def __is_valid(self):
		self.error_reason = "No error (Usually indicates a BUG)"
		self.p_from = Person.objects.get(id = int(self.from_id))
		if self.p_from == None:
			self.error_reason = "Non-existant seller"
			return False
		self.p_to = Person.objects.get(id = int(self.to_id))
		if self.p_to == None:
			self.error_reason = "Non-existant buyer"
			return False
		if self.amount <= 0:
			self.error_reason = "Cannot order zero"
			return False
		if self.p_to.has_swag(int(self.swag_id), int(self.amount)) == False:
			self.error_reason = "Buyer doesn't have enough items"
			return False
		# TODO: check for exceptions?
		return True

	def is_valid(self):
		b = self.__is_valid()
		self.save()
		return b

	def send(self):
		if self.is_valid == False:
			return False
		if settings.FEDINV_SEND_EMAILS == True:
			# Send the order to the person
			body = settings.FEDINV_ORDER_BODY %{
				"to": self.p_to.name,
				"from": self.p_from.name,
				"amount": self.amount,
				"swag": swag_id_to_name(self.swag_id)}
			send_mail(settings.FEDINV_ORDER_SUBJECT % {"from": self.p_from.name},
				body, settings.FEDINV_EMAIL_FROM, [self.p_to.email])
			# Send confirmation to the buyer
			body = settings.FEDINV_ORDER_CONFIRMATION_BODY %{
				"to":  self.p_to.name,
				"from": self.p_from.name,
				"amount": self.amount,
				"swag": swag_id_to_name(self.swag_id)}
			send_mail(settings.FEDINV_ORDER_CONFIRMATION_SUBJECT %{
				"from": self.p_from.name}, body, settings.FEDINV_EMAIL_FROM,
				[self.p_to.email])
		# TODO: record the Order somewhere
		return True
	
	def __unicode__(self):
		if self.is_valid():
			return "%s (%s) %s->%s" % (swag_id_to_name(self.swag_id),
				self.amount, self.p_from.name, self.p_to.name)
		else:
			return "Invalid order #%d" % self.id
	
	def dump(self):
		if self.is_valid():
			return "Id: %d From: %s To: %s Swag Name: %s Amount: %d" %(
				self.id, self.p_from.name, self.p_to.name,
				swag_id_to_name(self.swag_id), self.amount)
		else:
			return "Invalid Order: %s" %( self.error_reason)

	def get_error_reason():
		return error_reason


class Person(models.Model):
	id = models.IntegerField(primary_key = True)
	name = models.CharField(max_length=5000)
	team = models.IntegerField()
	password = models.CharField(max_length=500)
	email = models.CharField(max_length=500)
	# serialized with JSON
	held_swag = models.CharField(max_length=5000)

	@property
	def d_held_swag(self):
		return self.get_swag()

	def get_swag(self):
		return json.loads(self.held_swag)
	
	def set_swag(self, d_held):
		held_swag = json.dumps(d_held)

	def has_swag(self, swag_id, amount=1):
		swag_id = unicode(swag_id)
		amount = int(amount)
		if (swag_id in self.d_held_swag):
			if (int(self.d_held_swag[swag_id]) >= amount):
				return True
			else:
				return False
		else:
			return False

	def __unicode__(self):
		return self.name
