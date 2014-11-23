from django.http import HttpResponse
from django.template import RequestContext, loader
from django.template.defaulttags import register

from swag.models import SwagType, Person

@register.filter
def person_swag_amount(p, swag_id):
	if swag_id in p.d_held_swag:
		return p.d_held_swag[swag_id]
	return "0"

def index(request):
	return HttpResponse("Swag stuff will be here soon. <br /><a href='manage-swag'>Go this way until then</a>")

def manage_swag(request):
	t = loader.get_template('swag/all.html')
	c = RequestContext(request, {
		'region': "EMEA",
		'swag_list': SwagType.objects.all(),
	})
	return HttpResponse(t.render(c))

def edit_swag(request, swag_id):
	# Find ambassadors who have $swag_id
	plist = []
	for p in Person.objects.all():
		if (swag_id in p.d_held_swag):
			plist.append(p)

	t = loader.get_template('swag/edit-swag.html')
	c = RequestContext(request, {
		'region': "EMEA",
		'swag_id': swag_id,
		'plist': plist,
	})
	return HttpResponse(t.render(c))
