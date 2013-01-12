from django.db import models

class Version(models.Model):
	'''
	Guarda configuraciones para diferentes muestras
	del generador. Las opciones de configuracion
	estan en el `generador.Configuracion`
	
	Por defecto las configuraciones estan desactivadas,
	para activar una es necesario seleccionar la casilla
	"en uso" en el admin.Solamente debe existir una
	configuracion activada

	:param nombre: nombre de la configuracion *ex: cuba*
	:type nombre: string
	:param info: informacion adicional, no utilizada hasta el momento
	:type info: TextField
	:param en_uso: Esta en uso? solo debe existir uno marcado
	:type en_uso: Boolean
	'''
	nombre = models.CharField(max_length=300)
	info = models.TextField(blank=True)
	en_uso = models.BooleanField(default=True)
	
	def __unicode__(self):
		return self.nombre

	class Meta:
		verbose_name = 'Version'
		verbose_name_plural = 'Versiones'

class Unidad(models.Model):
	'''
	Unidades de conversion de valores, cada una tiene
	un valor(float), un signo ($, US$ etc..).
	La(s) unidad(es) seleccianadas para la actual
	configuracion

	:param nombre: nombre de la unidad *ex: dollar*
	:type nombre: string, max 50 char
	:param signo: caracter o identificador de la unidad *ex. $*
	:type signo: string max 10 char
	:param valor: valor de la unidad
	:type valor: float
	'''
	nombre = models.CharField(max_length=50)
	signo = models.CharField(max_length=10)
	valor = models.FloatField(blank=True)

	def __unicode__(self):
		return self.nombre

	class Meta:
		verbose_name = 'Unidad'
		verbose_name_plural = 'Unidades'

class Configuracion(models.Model):
	'''
	Configuraciones para los calculos del generador de 
	valores.

	:param version: ForeignKe a Version
	:param fecha_inicio: Fecha de inicio de la accion
	:type fecha_inicio: datetime
	:param valor_proyecto: valor del proyecto
	:type valor_proyecto: float
	:param valor_energia: valor de la energia
	:type valor_energia: float
	:param valor_papel: valor del papel
	:type valor_papel: float
	:param valor_hora_trabajo: valor de la hora de trabajo hombre
	:type valor_proyecto: float
	:param valor_simbolico: valor simobolico
	:type valor_simbolico: float
	:param valor_tintas: valor de las tintas e insumos
	:type valor_tintas: float
	:param porcentaje_devaluacion: porcentaje de devaluacion general
	:type porcentaje_devaluacion: float
	:param porcentaje_valuacion: porcentaje de valuacion general
	:type porcentaje_valuacion: float
	:param unidad: many2many a unidad
	:param ventana_inactividad: tiempo de inactividad del sistema
	:param unidad: int
	'''
	version = models.ForeignKey(Version)
	fecha_inicio = models.DateTimeField(blank=True,null=True)
	valor_proyecto = models.FloatField(blank=True,null=True)
	valor_energia = models.FloatField(blank=True,null=True)
	valor_papel = models.FloatField(blank=True, null=True)
	valor_hora_trabajo = models.FloatField(blank=True, null=True)
	valor_simbolico = models.FloatField(blank=True, null=True)
	valor_tintas = models.FloatField(blank=True, null=True)
	porcentaje_devaluacion = models.FloatField(blank=True,null=True)
	porcentaje_valuacion = models.FloatField(blank=True,null=True)
	unidad = models.ManyToManyField(Unidad, blank=True,null=True)
	ventana_inactividad = models.IntegerField(blank=True,null=True)

	def __unicode__(self):
		return "configuracion para "

	class Meta:
		verbose_name = 'Configuracion'
		verbose_name_plural = 'Configuraciones'

	
class TituloValor(models.Model):
	'''
	Cada uno de los titulos generados por la maquina.
	Se guardan en la base de datos el numero, fecha, 
	certificados *ssl* y *archivo fuente*.

	*son guardados los paths en el sistema*

	:param idenficador: numero serial del titulo generado
	:type identificador: int
	:param fecha_creacion: fecha de expedicion del titulo
	:type fecha_creacion: datetime
	:param certificado: path al certificado generado por *certificate_generator*
	:type certificado: path
	:param key: path al key generado por :py:mod: certificate_generator
	:type key: path
	:param fuente: archivo fuente usado para la impresion
	:type fuente: path
	'''
	identificador = models.IntegerField()
	fecha_creacion = models.DateTimeField()
	certificado = models.CharField(max_length=300)
	key = models.CharField(max_length=300)
	fuente = models.CharField(max_length=300)

	def __unicode__(self):
		return str(self.identificador)

	class Meta:
		ordering = ['-fecha_creacion']
		verbose_name = 'Titulo Valor'
		verbose_name_plural = 'Titulos Valores'

class Estado(models.Model):
	'''
	El estado de todo el sistema minuto a minuto.
	Son usados para generar las graficas informativas.
	
	:param timestamp: momento de generacion del reporte
	:type timestamp: datetime
	:param num_titulos_emitidos: numero total de titulos emitidos
	:type num_titulos_emitidos: int
	:param valor_unitario: valor de cada uno de los titulos emitidos
	:type valor_unitario: float
	:param tiempo_actividad: tiempo de actividad de la maquina
	:type tiempo_actividad: int 
	:param capital: capital al momento de guardar
	:type capital: float

	'''
	timestamp = models.DateTimeField()
	num_titulos_emitidos = models.IntegerField()
	valor_unitario = models.FloatField()
	tiempo_actividad = models.IntegerField()
	capital = models.FloatField()

	def __unicode__(self):
		return str(self.timestamp)

	class Meta:
		ordering = ['-timestamp']

