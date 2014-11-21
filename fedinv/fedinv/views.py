from django.http import HttpResponse
from django.template import RequestContext, loader 

def index(request):
	t = loader.get_template('home/index.html')
	c = RequestContext(request, {
		'region': "EMEA",
	})
	return HttpResponse(t.render(c))

def show_all_swag(request):
	t = loader.get_template('swag/all.html')
	c = RequestContext(request, {
		'region': "EMEA",
	})
	return HttpResponse(t.render(c))
