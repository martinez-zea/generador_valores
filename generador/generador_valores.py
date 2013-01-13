import datetime
from threading import Thread, Event, Lock
import logging
import time
import sys
from decimal import *

from certificate_generator import Certificate_generator
from template_writer import TemplateWriter
from web_api import WebApi
from serial_io import Serial_io


#connfiguracion del logger
logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',)

#configuracion de decimal
#precision de 7 decimales
getcontext().prec = 4
#redondeo hacia abajo
getcontext().rounding = ROUND_HALF_DOWN
#tiempo de actualizacion del estado en la bd en segundos
UPDATE_TIME = 60


class WatchAndPost(Thread):
    '''
    Clase encargada de contar el tiempo que lleva el app corriendo y cada
    mintuto postear el estado general y guardarlo en la base de datos.

    :param depreciacion: porcentaje de depreciacion, tomado de la bd
    '''

    def __init__(self, depreciacion):
        Thread.__init__(self)
        self.lock = Lock()
        self.name = 'WatchAndPost'
        self.stop = False
        self.loop = Event()

        self.api = WebApi()
        self.init_time = datetime.datetime.now()

        #variables globales del sistema
        self.current_time = datetime.datetime.now()
        self.last_post = datetime.datetime.now()
        self.num_titulos_emitidos = 0
        self.valor_unitario = 0.0
        self.capital = 0.0
        self.tiempo_actividad = 0
        self.depreciacion = depreciacion

        self.getLastEstado()

    def run(self):
        '''
        Funcion encargada de hacer cada 60 segundos un post a la base de datos
        con la informacion actualizada.Se calculan los valores de los titulos y
        del capital al cual se le aplica la depreciacion. Todos los valores se
        redondean a 8 decimales.

        Esta funcion llama a ``self.postUpdate`` que es la realmente encargada
        de hacer el POST a la base de datos
        '''
        try:
            while not self.loop.is_set():
                self.current_time = datetime.datetime.now()

                #depreciacion permanente
                depreciacion = (self.capital * self.depreciacion) / 100
                capital_depreciado = self.capital - depreciacion
                #redondea el capital a 8 decimales
                c_d = Decimal(capital_depreciado)

                self.capital = float(c_d.quantize(Decimal('.00000001')))
                logging.debug('depreciacion >>>> %s', depreciacion)

                #calcula valor unitario
                if not self.num_titulos_emitidos == 0:
                    #convierte a Decimal y redondea a 8 decimales
                    cap_dec = Decimal(self.capital)
                    num_dec = Decimal(self.num_titulos_emitidos)
                    div = cap_dec / num_dec

                    self.valor_unitario = \
                    float(div.quantize(Decimal('.00000001')))

                logging.debug(self.postUpdate(self.current_time,
                                        self.num_titulos_emitidos,
                                        self.valor_unitario,
                                        self.tiempo_actividad,
                                        self.capital))
                self.loop.wait(UPDATE_TIME)

        except Exception, err:
            logging.debug(err)
            sys.exit(0)

    def getLastEstado(self):
        '''
        Aquiere el ultimo valor de la base de datos y actualiza las variables
        internas de la clase con los datos recibidos. Esta funcion solamente se
        llama al inicio del programa para adquirir el ultimo estado guardado en
        el sistema y actualizar las variables internas de la clase.
        '''
        self.lock.acquire()
        try:
            response = self.api.get_estado(1)
            if response['meta']['total_count'] > 0:
                logging.debug('ultimo estado: %s', response)
                #actualiza las variables locales
                self.num_titulos_emitidos =\
                response['objects'][0]['num_titulos_emitidos']
                self.valor_unitario = response['objects'][0]['valor_unitario']
                self.capital = response['objects'][0]['capital']
                self.tiempo_actividad = response['objects'][0]['tiempo_actividad']

                self.last_post = datetime.datetime.now()
            else:
                #si es el primer objeto
                logging.debug('la bd esta vacia, inicializando valores')
                config = self.api.get_config(1)
                self.num_titluos_emitidos = 0
                self.valor_unitario = config['valor_proyecto']
                self.capital = config['valor_proyecto']
                self.tiempo_actividad = 0

                self.last_post = datetime.datetime.now()
        finally:
            self.lock.release()

    def postUpdate(self, current_time, num, valor, tiempo, capital):
        '''
        Toma los estados de las variables actuales y las envia al web app. Esta
        funcion se llama cada minuto en el run de esta clase
        '''
       # self.lock.acquire()
        try:
            response = self.api.post_estado(current_time,
                                    num, valor, tiempo, capital)
            return response

        except Exception, err:
            logging.debug(err)
            sys.exit(0)

    def quit(self):
        '''
        Cambia el flag interno de la clase para sacarlo del loop, terminal la
        funcion ``self.run()`` y poder terminar el hilo
        '''
        self.loop.set()

    def setNumTitulos(self, num):
        '''
        Actualiza (suma)  el numero de titulos emitidos

        :parmams num: num de titulos a sumar
        :type num: int
        :returns: total actualizado
        '''
        self.lock.acquire()
        try:
            self.num_titulos_emitidos += num
        finally:
            self.lock.release()

    def setNumTitulosPlus(self):
        '''
        Suma uno al valor total de titulos emitidos

        :return: total actualizado
        '''
        self.lock.acquire()
        try:
            self.num_titulos_emitidos += 1
        finally:
            self.lock.release()

    def setValorUnitario(self, num):
        '''
        Actualiza  (suma) el valor unitario de cada titulo
        * resta tambien??? entregando valor negativo????*

        :param num: valor a sumar
        :type num: float
        '''
        self.lock.acquire()
        try:
            self.valor_unitario += num
        finally:
            self.lock.release()

    def setCapital(self, num):
        '''
        Actualiza (suma) el capital del sistema

        :param num: valor a sumar
        :type num: float
        '''
        self.lock.acquire()
        try:
            self.capital += num
        finally:
            self.lock.release()

    def setTiempoActividad(self, num):
        '''
        Actualiza (suma) el tiempo de trabajo en segundos de operacion de la
        maqina

        :param num: segundos a sumar
        :type num: int
        '''
        self.lock.acquire()
        try:
            self.tiempo_actividad += num
        finally:
            self.lock.release()


class CreateCert(Thread):
    '''
    Clase que crea y firma los certificados criptograficos de cada titulo
    valor. Recibe en los parametros de inicializacion una instancia de la clase
    ``WatchAndPost`` para poder actualizar tanto el capital como el numero de
    titulos emitidos.

    :param w: Instancia de la clase ``WatchAndPost``
    :param simbolico: porcentaje del valor simbolico
    :param minuto: valor del minuto de trabajo
    :param tiempo: tiempo de trabajo de realizacion de cada bono

    '''
    def __init__(self, w, simbolico, minuto, tiempo):
        Thread.__init__(self)
        self.name = 'CreateCert'
        self.loop = Event()
        #evento para crear el titulo
        self.doit = Event()
        #inicializa en set el evento
        self.doit.set()
        #instancia de WatchAndPost
        self.watcher = w
        self.api = WebApi()
        self.tw = TemplateWriter(template='wolfram.jinja')
        self.ca = Certificate_generator('keys/generador.key',
                                        'keys/generador.crt')
        self.valor_simbolico = simbolico
        self.valor_minuto = minuto
        self.tiempo_trabajo = tiempo

    def run(self):
        '''
        Esta funcion corre en el fondo hasta ser llamada para crear el
        certificado -cuando llega un dato del puerto serial-. Internamente
        realiza los calculos del porcentaje a agregar al capital y actualiza
        los valores en el estado global del sistema.

        '''
        while not self.loop.is_set():
            #mantiene vivo el thread
            self.loop.wait(0.01)

    def quit(self):
        '''
        Cambia el flag interno para terminar la funcion ``self.run()`` y
        terminar el Thread
        '''
        self.loop.set()

    def create(self):
        logging.debug('generando certificado')
        logging.debug('numero de titulos %s', self.watcher.num_titulos_emitidos)

        #toma el tiempo y suma uno a los titulos
        now = datetime.datetime.now()
        self.watcher.setNumTitulosPlus()
        new_num = self.watcher.num_titulos_emitidos

        #actualiza el valor del capital
        percentage = (self.valor_minuto * self.valor_simbolico) / 100
        addToCapital = percentage * self.tiempo_trabajo
        self.watcher.setCapital(addToCapital)

        logging.debug('>>> valuacion: %s', addToCapital)
        logging.debug('nuevo numero de titulos %s', new_num)

        CA_response = self.ca.generate_and_sign('CO', 'Bogota', 'Bogota',
                        'generador de valores', 'generador de certificados',
                        str(new_num).zfill(9), new_num)

        logging.debug('certificado: %s', CA_response)

        source = self.tw.createSource(CA_response['certificate'],
                        str(new_num).zfill(9), now)

        new_post = self.api.post_valor(new_num, now,
                        CA_response['certificate'],
                        CA_response['key'],
                        source)
        logging.debug('nuevo cert', new_post)
        #al finalizar vuelve a poner el set en el evento
        #self.doit.set()

        return source


class SerialCom(Thread):
    def __init__(self, ca, watcher):
        Thread.__init__(self)
        self.name = 'SerialCom'
        self.loop = Event()
        self.ca = ca
        self.watcher = watcher
        #self.serial = Serial_io('/dev/ttyACM') #inicializa por defecto 'dev/ttyUSB'
        self.serial = Serial_io('/dev/ttyACM')
        self.isPrinting = False
        self.status = None

    def run(self):
        '''
        espera que orderCertificate sea True para crear el cert y enviarlo
        '''
        while not self.loop.is_set():
            #revisa constantemente el puerto serial
            self.serial.receive_data()

            #recibe la orden de crear el certificado
            if self.serial.orderCertificate == True:
                #crea el certificado
                cert = self.ca.create()
                logging.debug('cert: %s', cert)
                #lo envia a serial_id
                self.serial.open_certificate(cert)
                #cambia el flag
                self.serial.orderCertificate = False
                self.serial.send_data(20)
                self.isPrinting = True

            if self.isPrinting == True and self.serial.isPrinting == False:
                self.status = self.serial.report
                logging.debug('termino de imprimir: %s', self.status)
                #actualiza el tiempo en el sistema
                self.watcher.setTiempoActividad(self.status['print_duration'])
                self.isPrinting = False

            self.loop.wait(0.01)

    def quit(self):
        self.serial.close_com()
        self.loop.set()


def main():
    '''
    Instancia y ejecuta todos los threads del programa
    '''
    API = WebApi()
    #API = WebApi(url = 'http://generador/generador/api/v1')
    config = API.get_config(1)
    logging.debug(config)

    DEPRECIACION = config['porcentaje_devaluacion']
    CAPITAL_INICIAL = config['valor_proyecto']
    VALOR_SIMBOLICO = config['valor_simbolico']
    VALOR_MINUTO_TRABAJO = config['valor_hora_trabajo']
    #minutos
    TIEMPO_REALIZACION_TITULO = 5

    try:
        #inicializa los threads
        watcher = WatchAndPost(DEPRECIACION)
        watcher.start()
        ca = CreateCert(watcher,
                VALOR_SIMBOLICO,
                VALOR_MINUTO_TRABAJO,
                TIEMPO_REALIZACION_TITULO)
        ca.start()
        ser = SerialCom(ca, watcher)
        ser.start()
        while True:
            #simplemente mantiene vivo el MainThread para poder terminar el
            #proceso con cntr+c
            time.sleep(0.01)

    except KeyboardInterrupt:
        '''
        cntrl + c: termina los hilos y apaga el programa
        '''
        watcher.quit()
        watcher.join()
        ca.quit()
        ca.join()
        ser.quit()
        ser.join()

        sys.exit(1)

    except Exception, err:
        print err

if __name__ == '__main__':
    main()
