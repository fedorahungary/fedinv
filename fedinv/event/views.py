from django.http import HttpResponse
from django.template import RequestContext, loader

from event.forms import EventForm
from swag.models import SwagType

def index(request):
	t = loader.get_template('event/index.html')
	c = RequestContext(request, {
		'region': 'EMEA',
		'form': EventForm(),
		'allswag': SwagType.objects.all(),
	})
	return HttpResponse(t.render(c))
