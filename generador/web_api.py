import slumber

class WebApi():
    '''
    Clase para manejar la interaccion con el api del webapp via 
    el RESTful Api provisto.

    :params url: URL donde reside el API, si es instanciada sin parametros, el valor por defecto supone que la aplicacion esta corriendo en el servidor de prueba de Django.
    :type url: string
	'''
    #def __init__(self, url='http://localhost:8000/generador/api/v1/'):
    def __init__(self, url='http://generador/generador/api/v1'):
        self.url = url
        #objeto de coneccion con el api
        self.api = slumber.API(url)
        #variables que contienen los resources del api
        self.estado = self.api.estado
        self.valor = self.api.titulo_valor
        self.configuracion = self.api.configuracion
        self.version = self.api.version
        self.unidad = self.api.unidad

    def post_estado(self,timestamp,num_titulos, valor, tiempo, capital):
        '''
        recibe los datos necesarios para guardar el estado
        del sistema en la base de datos
        
        :param timestamp: tiempo del estado
        :type timestamp: datetime (la conversion a string se realiza en esta funcion)
        :param num_titulos: numero actual de titulos emitidos
        :type num_titulos: int
        :param valor_unitario: valor actual de cada titulo
        :type valor_unitario: float
        :param tiempo: tiempo de trabajo de la maquina
        :type tiempo: int
        :param capital: capital actual
        :type capital: float
        :returns: dict con la info del objeto creado
        '''
        now = timestamp.isoformat()
        return self.estado.post({'timestamp': now, 
							'num_titulos_emitidos': num_titulos, 
							'valor_unitario': valor, 
							'tiempo_actividad': tiempo, 
							'capital': capital})

    def post_valor(self,identificador,fecha,certificado,key, fuente):
        '''
        Recibe los datos necesarios para guardar un titulo valor
        generado en la base de datos

        :param identificador: numero del titulo a guardar
        :type identificador: int
        :param fecha: fecha emision
        :type fecha: datetime (la conversion a string se realiza en la funcion)
        :param certificado: path con el certificado generado para el titulo
        :type certificado: string (path)
        :param key: path con el key generado para el titulo
        :type key: string (path)
        :param fuente: archivo fuente del titulo 
        :type fuente: string (path)
        :returns: dict con la info del objeto creado
        '''
        fecha = fecha.isoformat()
        return self.valor.post({'identificador':identificador,
						  'fecha_creacion': fecha,
						  'certificado': certificado,
						  'key': key,
						  'fuente': fuente,})
    
    def get_estado(self,num_objs):
        '''
        Realiza una peticion GET al API que devuelve los ultimos X estados
        almacenados en la base de datos
        
        :param num_objs: numero de objetos a buscar
        :type num_objs: int
        :returns: dict con la respuesta
        '''
        return self.estado.get(limit=num_objs)

    def get_valor(self,num_objs):
        '''
        Realiza una peticion GET al API que devuelve los ultimos X titulos
        valores almacenados en la base de datos

        :param num_objs: numero de objetos a buscar
        :type num_objs: int
        :returns: dict con la respuesta
        '''
        return self.valor.get(limit=num_objs)

    def get_config(self,_id):
        '''
        Realiza una peticion GET al API que retorna los datos de la
        configuracion del sistema

        :param id: identificador de la configuracion
        :type id: int
        '''
        return self.configuracion(id=_id).get()
