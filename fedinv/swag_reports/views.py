from django.http import HttpResponse

from swag.models import SwagType

def index(request):
	return HttpResponse('Welcome to the Report section')

def by_team(request):
	return HttpResponse('By Team')

def amount(request):
	num = SwagType.objects.count()
	resp = "There are %d Swags" % num
	obj_set = SwagType.objects.all()
	for obj in obj_set:
		resp += "<br />%s: %d" %(obj.name, obj.amount)
	return HttpResponse(resp)
