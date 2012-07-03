from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^generador/', include('generador.urls')),
    # url(r'^app/', include('app.foo.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
