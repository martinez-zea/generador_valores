from django.conf.urls import patterns, url,include
from django.views.generic.simple import direct_to_template
from tastypie.api import Api
from generador.api import *

v1_api = Api(api_name='v1')
v1_api.register(VersionResource())
v1_api.register(ConfiguracionResource())
v1_api.register(UnidadResource())
v1_api.register(TituloValorResource())
v1_api.register(EstadoResource())

urlpatterns = patterns('',
		url('^$', direct_to_template, {'template' : 'viz_2.html'}),
		url('^api/', include(v1_api.urls)),
)
