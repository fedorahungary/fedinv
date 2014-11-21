from django.http import HttpResponse
from django.template import RequestContext, loader

from swag.models import SwagType

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
	return HttpResponse("Editing Swag: %s" % swag_id)
