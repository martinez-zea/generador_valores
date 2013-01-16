import time
import serial
import datetime
try:
    from serial.tools.list_ports import comports
except ImportError:
    comports = None


NUMBER_OF_CHARS = 1


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
        if comports:
            for pname in comports():
                if(pname[0].find(portpattern) == 0):
                    self.portname = pname[0]
                    #print portname

        try:
            self.port = serial.Serial(self.portname, 115200)
            print "Conexion abierta en: ", self.portname

        except Exception, error:
            print error

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
        print "current char: ", char
        self.port.write(char)

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
            print "NEXT STING: ", data
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
            print buff
            lines = buff.split('\n')
            if lines[-2]:
                datain = lines[-2]
                #sucio hack para lidiar con un 'invalid literal' cuando llega
                #algo de basura en por el serial
                try:
                    command = int(datain)
                except:
                    command = 0

                if command == 5:
                    ahora = time.time()
                    print 'tiempo: ', self.tiempo
                    print 'ahora: ', ahora
                    print 'resta: ', ahora - self.tiempo
                    #solo si han pasado 3 secs desde la ultima presion
                    if ahora - self.tiempo > 0.0:
                        self.tiempo = ahora
                        if self.isPrinting == False:
                            #pide el titulo
                            self.orderCertificate = True
                            self.isPrinting = True
                            self.start_time = datetime.datetime.now()
                            self.index = 0

                        else:
                            self.send_data(NUMBER_OF_CHARS)
                            self.presses += 1

            buff = lines[-1]
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
        #self.port.flush()

        #Clear output buffer, aborting the current output and discarding all that is in the buffer.
        #self.port.flushOutput()
        self.port.close()
