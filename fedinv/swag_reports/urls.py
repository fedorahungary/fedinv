from django.conf.urls import patterns, url

from swag_reports import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^all-swag/$', views.all_swag, name='report-all-swag'),
	url(r'^by-people/$', views.by_people, name='report-by-people'),
	url(r'^list-event/$', views.list_event, name='list-event'),
)
