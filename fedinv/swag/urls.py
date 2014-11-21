from django.conf.urls import patterns, url

from swag import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),

	url(r'manage-swag$', views.manage_swag, name='manage-swag'),

	url(r'edit-(?P<swag_id>\d+)/$', views.edit_swag, name='edit-swag'),
)
