import time
import serial
import datetime
try:
    from serial.tools.list_ports import comports
except ImportError:
    comports = None


class Serial_io:


    def __init__(self, portpattern = "/dev/ttyACM"):

        """
        Encuentra el puerto serial, con el patron definido en portpattern, abre
        la conexion serial
        """
        self.index = 0
        self.portpattern = portpattern # patron para buscar el puerto
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

        if comports:
            for pname in comports():
                if(pname[0].find(portpattern) == 0):
                    self.portname = pname[0]
                    #print portname

        try:
            self.port = serial.Serial(self.portname, 115200)
            print "Conexion abierta en" , self.portname

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
            data  = self.certxt[self.index:newindex]
            print data
            self.index = newindex
            self.cert = False

        self.port.write(data)
        self.port.flush()


    def receive_data(self):
        #lee el buffer del puerto serial hasta que encuentre un salto de linea,
        #pone todo lo que llega en un string y lo parte para sacar el dato
        buff = ''
        buff = buff + self.port.read(self.port.inWaiting())
        if '\n' in buff:
            lines = buff.split('\n')
            if lines[-2]:
                datain = lines[-2]
                #sucio hack para lidiar con un 'invalid literal' cuando llega
                #algo de basura en por el serial
                try:
                    command = int(datain)
                except:
                    command = 0

                if command  == 5:
                    if self.isPrinting == False:
                        self.orderCertificate = True #pide el titulo
                        self.isPrinting = True
                        self.start_time = datetime.datetime.now()
                        self.index = 0

                    else:    
                        self.send_data(5)
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
        work_time = self.presses* 10
        report = {'print_duration': delta_print.seconds, 
                'work_time': work_time} 

        return report


    def close_com(self):
        self.port.flush()
        self.port.close()


