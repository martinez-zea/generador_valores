import os
from OpenSSL import crypto


class Certificate_generator():
    '''
    Clase que interactua con OpenSSL para generar
    los certificados de autenticidad de cada
    titulo valor emitido por el generador

    Incializa la clase recibe los certificados
    del generador que seran usados para firmar los
    certificados expedidos

    :param priv_key: path al archivo con el private key
    :type priv_key: string (path)
    :param certificate: path al certificado del generador
    :type certificate: string (path)
    :param output_dir: directorio para guardar los archivos generados
    :type output_dir: strng (path)

    El codigo fue basado en: `http://www.themacaque.com/?p=1057 <http://www.themacaque.com/?p=1057>`_
    '''

    def __init__(self, priv_key, certificate, output_dir='output/certificates'):
        #crea los objectos SSL
        self.CA_privateKey = crypto.PKey()
        self.CA_certificate = crypto.X509()

        self.output_dir = output_dir
        #revisa si el directorio de salida existe, si no lo crea
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        #lee los archivos con la llave y certificado del CA
        with open(priv_key, 'r') as f:
            self.CA_privateKey = crypto.load_privatekey(crypto.FILETYPE_PEM, f.read())

        with open(certificate, 'r') as f:
            self.CA_certificate = crypto.load_certificate(crypto.FILETYPE_PEM, f.read())

    def generate_and_sign(self, c, st, l, o, ou, cn, serial):
        '''
        Funcion que expide y firma los certificados de cada
        titulo. Recibe todos los parametros necesarios para la
        generacion del certificado.

        :param c: sountry code, 2 caracteres
        :type c: string
        :param st: state o provincia
        :type st: string
        :param l: locality name
        :type l: string
        :param o: organization name
        :type o: string
        :param ou: organizational unit name
        :type ou: string
        :param cn: common name
        :type cn: string
        :param serial: numero de identificacion del titulo
        :type serial: int

        :returns: dictionary con path al certificado y llaves generado

        '''

        cert_path = os.path.join(self.output_dir, str(serial) + '.crt')
        key_path = os.path.join(self.output_dir, str(serial) + '.key')

        #crea el key para el certificado
        key = crypto.PKey()
        key.generate_key(crypto.TYPE_RSA, 1024)

        #genera el certificado para el titulo
        cert = crypto.X509()
        cert.get_subject().C = c
        cert.get_subject().ST = st
        cert.get_subject().L = l
        cert.get_subject().O = o
        cert.get_subject().OU = ou
        cert.get_subject().CN = cn
        cert.set_serial_number(serial)
        #activa la validez del certificado desde ahora
        #hasta dentro de 1000 anios
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)
        #agrega la info del CA al nuevo certificado
        cert.set_issuer(self.CA_certificate.get_subject())
        #agrega la llave creada para el certificado
        cert.set_pubkey(key)
        #firma el certificado con la llave del CA
        cert.sign(self.CA_privateKey, 'sha1')

        digest = cert.digest('md5')

        with open(cert_path, 'wt') as fd:
            fd.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

        with open(key_path, 'wt') as fd:
            fd.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))

        return {'certificate': cert_path, 
            'key': key_path,
            'digest': digest}
