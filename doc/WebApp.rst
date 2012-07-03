Aplicacion web
==============

La aplicacion esta escrita en `Django <http://djangoproject.org>`_, usa
Tastypie para hacer el API RESTfull que permite acceder a los datos
almacenados.

Los modelos estan guardados historicamente con `South
<http://south.aeracode.org/>`_ para iniciar la base de datos es necesario
primero correr el comando ``./manage syncdb`` y luego ``./manage migrate
generador`` para aplicar los cambios del modelo del app Generador.

======
Models
======

.. automodule:: generador.models
.. autoclass:: Version
    :members:
.. autoclass:: Unidad
    :members:
.. autoclass:: Configuracion
    :members:
.. autoclass:: TituloValor
    :members:
.. autoclass:: Estado
    :members:

===
Api
===

.. automodule:: generador.api
.. autoclass:: VersionResource
    :members:
.. autoclass:: UnidadResource
    :members:
.. autoclass:: ConfiguracionResource
    :members:
.. autoclass:: TituloValorResource
    :members:
.. autoclass:: EstadoResource
    :members:

============ 
TemplateTags
============
.. automodule:: generador.templatetags.verbatim
.. autoclass:: VerbatimNode
    :members:

