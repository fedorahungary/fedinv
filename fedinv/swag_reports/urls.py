from django.conf.urls import patterns, url

from swag_reports import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^all/$', views.amount, name='report-all'),
)
