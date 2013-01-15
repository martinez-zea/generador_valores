#!/opt/local/bin/python
import time
import serial

try:
    from serial.tools.list_ports import comports
except ImportError:
    comports = None


lorem = """\n\n\n\nLorem Ipsum Dolor sit amet, consEctEtur (---___--- ) adiPisiCing elit\n\n\n\n"""

index = 0

portpattern = "/dev/tty.usbmodem"  # patron para buscar el puerto

portname = None
certname = "test_certificate.txt"
certxt = None
port = None

open_serial()
open_certificate(certname)
presses = 0


def open_serial():
    """
    Encuentra el puerto serial, con el patron definido en portpattern
    """

    if comports:
        for pname in comports():
            if(pname[0].find(portpattern) == 0):
                portname = pname[0]
                #print portname

    try:
        global port
        port = serial.Serial(portname, 115200)
        print "Conexion abierta en ", portname
    except Exception, error:
        print error


def open_certificate(filename):
    try:
        with open(certname, 'r') as f:
            global certxt
            certxt = f.read()

    except Exception, error:
        print error


def send_txt(numchars):
    global index
    newindex = index + numchars
    data = ''
    if newindex > len(certxt):
        #data = lorem[0:numchars]
        data = '\x03'
    else:
        data = certxt[index:newindex]
    print 'text sent'
    index = newindex
    port.write(data)
    port.flush()


def main():
    try:
        while True:
            if port.inWaiting() > 0:
                datain = port.read(1)
                print datain
                print type(datain)
                command = int(datain)
                if command == 5:
                    send_txt(5)
                    #break
                else:
                    print "entra: ", command

    except KeyboardInterrupt:
        port.flush()
        port.close()

if __name__ == '__main__':
    main()
