Dispensador de valores es una obra de proceso que involucra tecnología e
interacción entre los asistentes a la Bienal de la Habana.  El trabajo consiste
en un sistema de producción e intercambio de objetos artísticos (impresiones
tipográficas en papel) creados con una máquina especial, basada en una máquina
de escribir eléctrica modificada.  Los objetos producidos serán pequeños
grabados, que serán producidos en esta máquina, la que será diseñada y
construida por nosotros para este proyecto.


Esta máquina podrá ser operada en el espacio de exhibición por los visitantes.
Al operar el dispositivo se podrán imprimir copias de un grabado hecho con
tipos móviles, algunas partes de la imagen serán iguales en todas las copias, y
otras partes serán únicas en cada copia, gracias a un sistema de variabilidad
implementado en la máquina.  La idea es que cada impresión creada en la máquina
tendrá un precio que podrá variar según dos indicadores:  el tiempo de trabajo
invertido cada copia y el numero de copias existentes. El precio del objeto
será registrado y publicado en un sitio web, actualizado por un sistema
incluido en la máquina.  En este se podrá verificar cual es el precio actual
del trabajo en comparación a otra moneda (dolares, bitcoins, peso cubano o
similar ).

Marco conceptual
================

El trabajo gira entorno a la relación entre valor estético y valor económico de
la obra, al igual que cuestiona la naturaleza de la interacción entre un humano
y una máquina en el contexto del museo y las artes electrónicas.  La máquina
esta diseñada para requerir trabajo físico y repetitivo del interactor con el
objetivo de poner en marcha el proceso de creación y producción de una
impresión tipográfica, que es al mismo tiempo un objeto artístico y documento.
La impresión esta realizada con una máquina de escribir automática conectada a
un pequeño computador, programado para crear patrones visuales compuestos de
caracteres.  El patrón, único en cada copia, es el valor diferencial entre
copias y le otorga un elemento de unicidad.  Al mismo tiempo, parte del impreso
llevará información sobre la producción misma del objeto, como la hora y fecha
de emisión, el tiempo que tomo construirlo, y otros datos que dan testimonio de
la creación del objeto.  

Este objeto es a su vez el producto de la interacción, y el testimonio de la
misma.  La instalación interactiva es la máquina que produce el objeto, y la
interacción es la aplicación de una fuerza de trabajo para producirlo.  El
objeto cristaliza el esfuerzo colectivo entre la máquina y la persona y por
ende guarda parte  del valor estético y económico asociado al trabajo.  Este
valor no es únicamente simbólico, sino que es potencialmente capital. Cada
copia tiene un precio, que esta basado en los costos de producción de la
máquina mas los costos de producción de una copia, dividido en el numero de
copias existentes.  De esta forma, cada vez que se produzca una copia, el
precio de todas las copias se reducirá, pues el valor del trabajo se reparte
entre los poseedores del grabado.  Para registrar las impresiones y actualizar
los precios se usará una aplicación web que se conecta a la máquina y recibe
las actualizaciones.  Este precio podrá ser convertido a diferentes monedas,
pero también podrá ser intercambiado por las personas en intercambios por otros
bienes o servicios.

La idea detrás del proyecto es crear una infraestructura en pequeña escala,
para producir y circular valor económico y simbólico, a partir de la producción
de objetos artísticos y del trabajo invertido en ellos.  La intención es crear
un trabajo que pueda trascender la noción de obra interactiva que funciona y
adquiere sentido únicamente en el contexto temporal y espacial de la sala de
exhibición.  Nos interesa plantear la interacción como un trabajo que genera
valor estético y económico, pero también la posibilidad de generar un espacio
de intercambio entre quienes interactúan con la obra.

Descripción técnica
===================

La obra contará con dos partes, la primera será un dispositivo electrónico y
mecánico que realizará las labores de impresión y será activado por los
asistentes a la exposición, el segundo componente será una pagina web que
almacenará los datos de cuantos impresos se han realizado junto al valor de
cada uno, esta información estará disponible para que sea distribuida por otros
canales diferentes a Internet de mayor acceso en el contexto especifico de la
Bienal.

El dispositivo de impresión será construido a partir de la molificación de una
máquina de escribir eléctrica, la cual será controlada usando un software
escrito para el proyecto que estará encargado de generar los patrones a
imprimir sobre el papel, este usará algoritmos para la creación de imágenes
generativas tales como autómatas celulares, lo que permitirá crear patrones que
para cada ejecución serán diferentes, pero mantendrán cierta unidad entre si.

para funcionar, la máquina requerirá que los visitantes la activen usando una
rudimentaria palanca, que estará integrada en el cuerpo del sistema. La
interacción controlará la ejecución de cada ciclo del programa, de esta manera
será necesario que el visitante la accione hasta completar la impresión, una
vez concluido el proceso podrá llevase con sigo la copia.

Por otra parte, el software que controlará la máquina tendrá la misión de
contar el numero de piezas impresas y realizar los cálculos correspondientes
para establecer el precio unitario en relación a la cantidad de copias
existentes. Esta información será actualizada en tiempo real en una pagina en
Internet, que a su vez se encontrará proyectada sobre una pared de la sala.
Estos indicadores podrán exportarse en diferentes formatos para facilitar su
difusión por otros medios.

El software, diseño de hardware y planos de construcción del dispositivo, serán
liberados en el sitio web del proyecto amparados por una licencia libre. 
