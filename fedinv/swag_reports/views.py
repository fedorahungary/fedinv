from django.http import HttpResponse
from django.template import RequestContext, loader

from fedinv import settings, fedinv
from swag.models import SwagType, Person
from event.models import InvEvent
from swag_reports.models import Report

def index(request):
	template = loader.get_template("reports/index.html")
	context = RequestContext(request, {
		'region': settings.FEDINV_REGION,
		'reports': Report.objects.all(),
	})
	return HttpResponse(template.render(context))

def by_team(request):
	return HttpResponse('By Team')

def by_people(request):
	template = loader.get_template("reports/by-person.html")
	context = RequestContext(request, {
		'region': settings.FEDINV_REGION,
		'person_list': Person.objects.all(),
	})
	return HttpResponse(template.render(context))

def list_event(request):
	template = loader.get_template("reports/events.html")
	context = RequestContext(request, {
		'region': settings.FEDINV_REGION,
		'events': InvEvent.objects.all(),
	})
	return HttpResponse(template.render(context))

def all_swag(request):
	obj_set = SwagType.objects.all()
	users = Person.objects.all()
	# Ideally, we shouldn't recount on every request,
	# We need some caching...
	if fedinv.swag_cache_valid == False:
		for s in obj_set:
			s.old_amount = s.amount
			s.amount = 0
			for p in users:
				s.amount += p.get_swag_amount(s.id)
			s.save()
	fedinv.swag_cache_valid = True

	template = loader.get_template("reports/all.html")
	context = RequestContext(request, {
		'region': settings.FEDINV_REGION,
		'obj_list': obj_set,
	})
	return HttpResponse(template.render(context))
