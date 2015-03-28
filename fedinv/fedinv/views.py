from django.http import HttpResponse
from django.template import RequestContext, loader 
from django.contrib.auth import logout
from django.shortcuts import redirect

import settings

def index(request):
	t = loader.get_template('home/index.html')
	c = RequestContext(request, {
		'region': settings.FEDINV_REGION,
		'is_auth': request.user.is_authenticated(),
		'user_name': request.user.username,
	})
	return HttpResponse(t.render(c))

def logout_me(request):
	logout(request)
	return redirect("/")
