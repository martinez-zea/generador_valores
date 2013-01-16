import time
import serial
import datetime
import sys
try:
    from serial.tools.list_ports import comports
except ImportError:
    comports = None


NUMBER_OF_CHARS = 32
DELAY_TIME = 0.20


class Serial_io:
    def __init__(self, portpattern="/dev/ttyACM"):

        """
        Encuentra el puerto serial, con el patron definido en portpattern, abre
        la conexion serial
        """
        self.index = 0
        #patron para buscar el puerto
        self.portpattern = portpattern
        self.portname = None
        self.certname = None
        self.certxt = None
        self.port = None
        self.presses = 0
        self.print_time = None
        self.print_duration = None
        self.start_time = None
        self.isPrinting = False
        self.orderCertificate = False
        self.report = None
        self.tiempo = time.time()
        self.printer_buffer = []
        if comports:
            for pname in comports():
                if(pname[0].find(portpattern) == 0):
                    self.portname = pname[0]
                    #print portname

        try:
            self.port = serial.Serial(self.portname, 115200)
            print "Open connection on: ", self.portname

        except Exception, error:
            print error
            sys.exit("Error trying to connect to serial port")

    def open_certificate(self, filename):
        '''
        abre el certificado y lo guarda en un string
        '''
        self.certname = filename
        try:
            with open(self.certname, 'r') as f:
                self.certxt
                self.certxt = f.read()
                print self.certxt

        except Exception, error:
            print error

    def write_character(self, char):
        #print "current char: ", char
        self.port.write(char)
        time.sleep(DELAY_TIME)

    def send_data(self, numchars):
        '''
        Envia el texto por serial cuando el microcontrolador lo solicita
        '''
        newindex = self.index + numchars
        data = ''
        if newindex > len(self.certxt):
            #el proximo es un nuevo certificado
            data = '\x03'
            self.isPrinting = False
            self.report = self.report_status()
        else:
            self.isPrinting = True
            data = self.certxt[self.index:newindex]
            print "NEXT STRING: ", data
            self.index = newindex
            self.cert = False

        for character in data:
            self.write_character(character)
        #self.port.write(data)
        #self.port.flushOutput()

    def receive_data(self):
        #lee el buffer del puerto serial hasta que encuentre un salto de linea,
        #pone todo lo que llega en un string y lo parte para sacar el dato
        buff = ''

        try:
            buff = buff + self.port.read(self.port.inWaiting())
        except IOError:
            self.close_com()
            self.port = serial.Serial(self.portname, 115200)
            print("IOERROR: REINICIANDO SERIAL ::::::::::::::::::::::::::")
        if '\n' in buff:
            #init var with random data
            lever = sensor_1 = sensor_2 = 9
            try:
                lever = buff[0]
                sensor_1 = buff[1]
                sensor_2 = buff[2]
                print "::::: Serial Data Arrived! ::::::"
                print "Lever: ", lever
                print "Sensor 1: ", sensor_1
                print "Sensor 2: ", sensor_2

            except Exception, error:
                print error
                pass

            if lever == '5':
                ahora = time.time()
                print 'tiempo: ', self.tiempo
                print 'ahora: ', ahora
                print 'resta: ', ahora - self.tiempo
                #solo si han pasado 3 secs desde la ultima presion
                if ahora - self.tiempo > 0.0:
                    self.tiempo = ahora
                    if self.isPrinting == False and sensor_1 == '1' and sensor_2 == '0':
                        print "Starting new certificate"
                        #pide el titulo
                        self.orderCertificate = True
                        self.isPrinting = True
                        self.start_time = datetime.datetime.now()
                        self.index = 0
                       
                        for a in range(12):
                            self.write_character('\n')


                    elif self.isPrinting == False and sensor_1 == '0' and sensor_2 == '1':
                        print "waiting to remove paper"
                        pass

                    elif self.isPrinting == True and sensor_1 == '0' and sensor_2 == '0':
                        print "sheet removed before finish"
                        pass

                    elif self.isPrinting == True:
                        print "Send data to printer"
                        self.send_data(NUMBER_OF_CHARS)
                        self.presses += 1
            #reset vars
            lever = 9
            #report = self.report_status()
            #return report

    def report_status(self):
        '''
        evalua si se acabo el certificado y cuanto tiempo tomo en ser
        impreso y cuanto tiempo de trabajo se requirio

        :returns: diccionario con el tiempo de impresion y el tiempo de trabajo
        '''
        #calcula el tiempo entre el inicio y finalizacion de impresion
        end_time = datetime.datetime.now()
        delta_print = end_time - self.start_time

        #tiempo de trabajo, por ahora en presiones * 10
        work_time = self.presses * 10
        report = {'print_duration': delta_print.seconds,
                'work_time': work_time}

        return report

    def close_com(self):
        #Clear output buffer, aborting the current output and discarding all that is in the buffer.
        self.port.flushOutput()
        self.port.close()
