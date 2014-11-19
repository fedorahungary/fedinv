from django.http import HttpResponse
from django.template import RequestContext, loader

from swag.models import SwagType, Person
from swag_reports.models import Report

def index(request):
	template = loader.get_template("reports/index.html")
	context = RequestContext(request, {
		'region': "EMEA",
		'reports': Report.objects.all(),
	})
	return HttpResponse(template.render(context))

def by_team(request):
	return HttpResponse('By Team')

def by_people(request):
	template = loader.get_template("reports/by-person.html")
	context = RequestContext(request, {
		'region': "EMEA",
		'person_list': Person.objects.all(),
	})
	return HttpResponse(template.render(context))

def all_swag(request):
	num = SwagType.objects.count()
	resp = "There are %d Swags" % num
	obj_set = SwagType.objects.all()
	template = loader.get_template("reports/all.html")
	context = RequestContext(request, {
		'region': "EMEA",
		'obj_list': obj_set,
	})
	return HttpResponse(template.render(context))
