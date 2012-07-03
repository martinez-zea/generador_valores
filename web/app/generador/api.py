from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.authorization import Authorization
from generador.models import *

class VersionResource(ModelResource):	
	'''
	Crea el recurso para todas las versiones.
	Solamente tiene permisos para *get*

	Es posible filtrarlas usando el parametro: ``/version/?en_uso=true``
	'''
	configuracion = fields.ToManyField('generador.api.resources.ConfiguracionResource', 'configuracion')
	class Meta:
		queryset = Version.objects.all()
		resource_name = 'version'
		filtering ={
				"en_uso": ('exact'),
				}

class UnidadResource(ModelResource):
	'''
	Recurso para acceder a las unidades almacenadas en la base de datos.
	se obtienen todos los elementos.
	'''
	configuracion = fields.ToManyField('generador.api.resources.ConfiguracionResource', 'configuracion')
	class Meta:
		queryset = Unidad.objects.all()
		resource_name = 'unidad'

class ConfiguracionResource(ModelResource):
	'''
	Recurso para listar las configuraciones del sistema.
	En relacion via FK con *VersionResource*
	'''
	version = fields.ToOneField(VersionResource, 'version')
	unidad = fields.ToManyField(UnidadResource, 'unidad')
	class Meta:
		queryset = Configuracion.objects.all()
		resource_name = 'configuracion'
        filtering = {
                'id' :('exact'),
                }

class TituloValorResource(ModelResource):
	'''
	Recurso para acceder a los titulos valores via ``/titulo_valor/``
	Se pueden filtrar via fecha de creacion:

	:key exact: busqueda exacta
	:key range: rango de elementos
	:key year: listado por anios
	:key month: listado por meses
	:key day: listado por dias
	:key week_day: listado por dias de la semana

	Por identificador:

	:key exact: numero exacto del TV
	:kep in: rango de elementos

	'''
	class Meta:
		queryset = TituloValor.objects.all()
		resource_name = 'titulo_valor'
		authorization = Authorization()
		filtering = {
				'identificador':('exact', 'in'),
				'fecha_creacion': ('exact', 'range', 'year', 'month', 'day', 'week_day'),
				}

class EstadoResource(ModelResource):
	'''
	Recurso para acceder a los estados del sistema via ``/estado/``.
	Cada query esta paginado por 60 elementos.
	
	Se pueden filtrar via timestamp:

	:key exact: busqueda exacta
	:key range: rango de elementos
	:key year: listado por anios
	:key month: listado por meses
	:key day: listado por dias
	:key week_day: listado por dias de la semana
	:key lt: menor a la fecha indicada
	:key lte: menor o igual a la fecha indicada
	:key gt: mayor a la fecha indicada
	:key gte: mayor o igual a la fecha indicada
	:key contains: contiene el termino entregado

	Por numero de titulos emitidos:

	:kep in: rango de elementos

	Por valor unitario, tiempo de actividad y capital:

	:key exact: busqueda exacta
	:key lt: menor al valor indicado
	:key lte: menor o igual al valor indicado
	:key gt: mayor al valor indicado
	:key gte: mayor o igual al valor indicado
	:key contains: contiene el termino entregado


	'''

	class Meta:
		queryset = Estado.objects.all()
		resource_name = 'estado'
		authorization = Authorization()
		filtering ={
				'timestamp':('exact', 'range', 'year', 'month', 'day', 'week_day', 'lt', 'lte', 'gt', 'gte', 'contains'),
				'num_titulos_emitidos': ('in',),
				'valor_unitario':('in', 'exact', 'lt', 'lte', 'gt', 'gte'),
				'tiempo_actividad': ('in', 'exact', 'lt', 'lte', 'gt', 'gte'),
				'capital' : ('in', 'exact', 'lt', 'lte', 'gt', 'gte')
				}

