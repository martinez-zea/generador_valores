import os
from random import randint
from jinja2 import Environment, PackageLoader
from wolfram import Wolfram

class TemplateWriter():
    '''
    Clase que interactua con Jinja2. el sistema de templates empleado para la
    generacion de cada uno de los titulos impresos. 
    
    :param package: el paquete a usar, por defecto es generador
    :type package: string
    :param template_dir: directorio donde estan los templates a usar
    :type template_dir: string
    :param output_dir: directorio donde se colocan los archivos procesados
    :type output_dir: string
    '''
    def __init__(self, package='generador_valores', template_dir='templates',
                                                template='baselower.jinja',
                                                output_dir='output/titulos'):
        self.package = package
        self.template_dir = template_dir
        self.template = template
        self.output_dir = output_dir
        
        #cellular automatas
        self.pattern1 = Wolfram(num_cells=9)
        self.pattern2 = Wolfram(num_cells=4)
        self.pattern3 = Wolfram(num_cells=3)

        #si no existe el directorio de salida lo crea
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        #inicializa el template engine
        self.environment = Environment(loader=PackageLoader(self.package,
                                                      self.template_dir))
        self.environment.filters['crt_title'] = self.crt_title
        self.base_template = self.environment.get_template(self.template)

    def crt_title(self,value):
        '''
        Filtro para centrar la primera y ultima linea del string
        entregado
        
        :param value: El strig a centrar
        :type value: string 
   
        '''
        tmp = value.splitlines(True)
        tmp[0] = tmp[0].rstrip().center(28)+'\n'
        tmp[len(tmp)-1] = tmp[len(tmp)-1].rstrip().center(64)+'\n'
        return ''.join(tmp)

    def createSource(self, certificate, serial, date):
        '''
        Inyecta en el template la info entregada en las variables y escribe un
        archivo el resultado.

        :param certificate: path al archivo del certificado
        :type certificate: string (path)
        :param serial: numero de identificacion
        :type serial: string (8 caracteres)
        :param date: fecha de emision del titulo
        :type date: datetime.datetime
        
        :returns: el path al certificado creado
        '''
        src_path = os.path.join(self.output_dir, serial+'.txt')
        #formatea la fecha
        date = date.strftime('%d/%m/%Y %H:%M')
        #lee el certificado
        with open(certificate, 'r') as f:
            crt = f.read()
        #crea los patrones 
        pttrn1 = self.translate_pattern1()
        pttrn2 = self.translate_pattern2()
        pttrn3 = self.translate_pattern3()
        borla = self.borla()
        capitel = self.capitel()

        #inyecta los datos
        src = self.base_template.render(certificate=crt.lower(),
                                        serial=serial,
                                        date = date,
                                        pattern1 = pttrn1,
                                        pattern2 = pttrn2,
                                        pattern3 = pttrn3,
                                        borla = borla,
                                        capitel = capitel)
        #escribe en el archivo
        with open(src_path, 'wt') as fd:
            fd.write(src.encode('utf-8'))
        
        return src_path

    def translate_pattern1(self):
        pttrn = self.pattern1.generate()
        final = ''
        for c in pttrn:
            if c == 0:
                final += '-'
            if c == 1:
                final += '='
            if c == 2:
                final += '.'
            if c == 3:
                final += ';'
            if c == 4:
                final += ','
        return final

    def translate_pattern2(self):
        pttrn = self.pattern2.generate()
        final = ''

        for c in pttrn:
            if c == 0:
                final += '-'
            if c == 1:
                final += '='
            if c == 2:
                final += '!'
            if c == 3:
                final += '='
            if c == 4:
                final += '-'
        return final

    def translate_pattern3(self):
        pttrn = self.pattern2.generate()
        final = ''

        for c in pttrn:
            if c == 0:
                final += '!'
            if c == 1:
                final += '='
            if c == 2:
                final += '!'
            if c == 3:
                final += '-'
            if c == 4:
                final += '='
        return final

    def borla(self):
        options = ['6', '8', '9', '0']
        return options[randint(0,len(options)-1)]

    def capitel(self):
        options = ['!', '-', '=', ';', '.', ',']
        c = options[randint(0,len(options)-1)]
        final =''
        for i in range(5):
            final +=c

        return final

