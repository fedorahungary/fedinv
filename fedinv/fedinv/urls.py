from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fedinv.views.home', name='home'),
    # url(r'^fedinv/', include('fedinv.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^$', 'fedinv.views.index', name='index'),

    url(r'^openid/', include('django_openid_auth.urls')),
    url(r'^logout/$', 'fedinv.views.logout_me'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Swag subsite
    url(r'^swag/', include('swag.urls')),

    # Reports subsite
    url(r'^report/', include('swag_reports.urls')),

    # Event subsite
    url(r'^event/', include('event.urls')),
)
