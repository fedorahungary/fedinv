from django.http import HttpResponse
from django.template import RequestContext, loader

def index(request):
	t = loader.get_template('event/index.html')
	c = RequestContext(request, {
		'region': 'EMEA',
	})
	return HttpResponse(t.render(c))