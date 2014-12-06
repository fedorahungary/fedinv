from django.conf.urls import patterns, url

from event import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
)
