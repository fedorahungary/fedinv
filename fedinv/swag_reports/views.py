from django.http import HttpResponse
from django.template import RequestContext, loader

from fedinv import settings
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
	num = SwagType.objects.count()
	resp = "There are %d Swags" % num
	obj_set = SwagType.objects.all()
	template = loader.get_template("reports/all.html")
	context = RequestContext(request, {
		'region': settings.FEDINV_REGION,
		'obj_list': obj_set,
	})
	return HttpResponse(template.render(context))
