from django.http import HttpResponse
from django.template import RequestContext, loader 

import settings

def index(request):
	t = loader.get_template('home/index.html')
	c = RequestContext(request, {
		'region': settings.FEDINV_REGION,
	})
	return HttpResponse(t.render(c))


