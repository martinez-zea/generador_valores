Hardware
========

Beagleboard
===========

instalacion
-----------
#. La SD debe prepararse con dos particiones una FAT-16 de 128m y otra EXT3 con
   el resto del espacio para guardar el sistema de archivos y los datos.
#. Descargar el `Bootloader <http://archlinuxarm.org/os/omap/BeagleBoard-bootloader.tar.gz>`_
   copiarlo a la particion FAT y descomprimirlo
#. Descargar la ultima version del `root file system
   <http://archlinuxarm.org/os/ArchLinuxARM-omap-smp-latest.tar.gz>`_ y
   descomprimirlo como **root** en la particion EXT3
#. Copiar ``/boot/uImage`` del root file system a la particion FAT
#. Crear un archivo ``boot.scr`` con el siguiente contenido:
   ::
    
    setenv bootargs 'console=ttyO2,115200n8 omapfb.mode=dvi:1024x768MR-16@60
    omapdss.def_disp=dvi root=/dev/mmcblk0p2 rw rootfstype=ext3 
    rootwait' 
    mmc init 
    fatload mmc 0 0x80300000 uImage 
    bootm 0x80300000 
    boot
    
   Para modificar el tamano del monitor a usar, es necesario modificar la
   directiva ``omapfb.mode=dvi:1024x768MR-16@60`` y colocar la respectiva
   resolucion y tasa de refresco del monitor a usar
#. Usar ``mkimage`` para crear el archivo ``boot.scr`` que luego sera copiado a la
   partcion FAT de la SD ::

    mkimage -A arm -O linux -T script -C none -a 0 -e 0 -n "Beagleboard boot
    script" -d bootcmd boot.scr

#. Copiar el archivo generado a la particion FAT

#. Crear swap file (se puede hacer desde la beagle)::
    
    dd if=/dev/zero of=/swapfile.img bs=1M count=512 #for a 1GB swapfile, use count=1024 
    mkswap /swapfile.img

  activarla con: ::
    
    swapon /swapfile.img

  Agregarla al ``/etc/fstab``: ::
    
    /swapfile.img none swap sw 0 0


Paquetes
--------
La instalacion minima debe tener:

* python-2.7
* cherokee
* python2-virtualenv
* midori (u otro navegador como uzbl)
* mercurial
* openSSH (para conexiones remotas)
* openSSL
* gcc

Entorno grafico:

* xorg-server 
* xorg-xinit 
* xorg-server-utils 
* xf86-video-fbdev
* dbus
* lxde (group)
* lxdm


Opcionales pero utiles:

* vim
* zsh
* git
* screen
* htop

Configuracion del sistema
-------------------------

/home/mz
^^^^^^^^
* El usuario ``http`` debe tener permisos para ejectuar y guardar cosas en el
  home, es necesario hacer un: ::
    
    chmod 775 /home/mz

  lo mismo para las carpetas ``env/biv`` ``web/app/`` y la base de datos puede
  tener un ``chmod 777 database.db``

* Verificar que en ``settings.py`` la ruta de la base de datos no este
  relativa, debe ser completa.

/home/mz/.config
^^^^^^^^^^^^^^^^
Crear la carpeta de configuracion de openbox y copiar archivos de
configuracion: ::
    
    mkdir -p ~/.config/openbox
    
    cp /etc/xdg/openbox/{rc.xml,menu.xml,autostart,environment}
    ~/.config/openbox

/home/mz/.config/autostart
^^^^^^^^^^^^^^^^^^^^^^^^^^

Configuracion de inicio de Openbox, en el repositorio de software en la carpeta
``beagleBoard/home_config`` se encuentran tanto el ``autostart`` como el ``menu.xml``
actualizados a la version en uso.

::

    #
    # These things are run when an Openbox X Session is started.
    # You may place a similar script in $HOME/.config/openbox/autostart
    # to run user-specific things.
    #

    #prevenir que el monitor se duerma
    xset -dpms s off &

    #lanza el app en fullscreen
    uzbl-browser -g maximixed http://generador.local.lab/generador/ &
   

/etc/rc.conf
^^^^^^^^^^^^

Seciones relevantes del archivo: ::

    TIMEZONE="America/Havana"
    HOSTNAME="generador"
    DAEMONS=(hwclock syslog-ng network netfs crond sshd cherokee)


/etc/hosts
^^^^^^^^^^
El local host debe tener un alias ``generador.local.lab`` para que resuelva
localmente la aplicacion en el servidor ::
    
    #
    # /etc/hosts: static lookup table for host names
    #

    #<ip-address>   <hostname.domain.org>   <hostname>
    127.0.0.1       localhost.localdomain   localhost
    127.0.0.1       generador.local.lab     generador

    ::1             localhost.localdomain   localhost

    # End of file

/etc/inittab
^^^^^^^^^^^^

::

        ## Only one of the following two lines can be uncommented!
        # Boot to console
        #id:3:initdefault:
        # Boot to X11
        id:5:initdefault:

        # Example lines for starting a login manager
        #x:5:respawn:/usr/bin/xdm -nodaemon
        #x:5:respawn:/usr/sbin/gdm -nodaemon
        #x:5:respawn:/usr/bin/kdm -nodaemon
        #x:5:respawn:/usr/bin/slim >/dev/null 2>&1
        x:5:respawn:/usr/bin/lxdm >/dev/null 2>&1

/etc/lxdm/lxdm.conf
^^^^^^^^^^^^^^^^^^^
Habilitar el autologin: ::
    
    autologin=mz

Tambien es necesario eliminar el password de la cuenta para que LXDM no exiga
el password al inciar: ::

     passwd -d  mz

Editar el ``/etc/pam.d/lxdm`` y dejarlo asi: ::
    
    auth    required    pam_unix.so nullok


/etc/cherokee/cherokee.conf
^^^^^^^^^^^^^^^^^^^^^^^^^^^

En cherokee se debe crear un virtual host que apunte a ``generador.local.lab``
usando el asistente y seleccionando el wizard para Django. Una vez creado se
modifica en ``Behavior Rules`` el apartado ``/media`` agregandole una ruta
adicional de directorios a buscar con un *or* apuntando a ``/static`` el
document root de esta rega debe apuntar a
``/home/mz/generador_valores/web/app/generador/static``

La otra cuestion a revisar es el interprete a usar por el Vhost, para esto en
``Behavior->Default->handler`` en la parte inferior esta un link a information
sources, al darle click se puede editar la regla, en el interprete para que
quede asi:::

     /home/mz/generador_valores/env/bin/python
     /home/mz/generador_valores/web/app/manage.py runfcgi protocol=scgi
     host=127.0.0.1 port=54487

Adicionalmente en la casilla **usuario** se debe poner ``mz`` y en la de
**grupo** ``users``, de esta manera no hay lios con los permisos de lectura y
escritura de los folders de la aplicacion. El unico cambio importante de
permisos es en la carpeta ``/home/mz`` a la cual se le deben cambiar los
permisos, un ``chmod 775 /home/mz`` deberia ser suficiente. 

De cualquier manera este es el ``cherokee.conf`` generado con la configuracion
anterior:::

    config!version = 001002101
    server!bind!1!port = 80
    server!group = http
    server!keepalive = 1
    server!keepalive_max_requests = 500
    server!panic_action = /usr/bin/cherokee-panic
    server!pid_file = /var/run/cherokee.pid
    server!server_tokens = full
    server!timeout = 15
    server!user = http
    vserver!10!directory_index = index.html
    vserver!10!document_root = /srv/http
    vserver!10!error_writer!filename = /var/log/cherokee/cherokee.error
    vserver!10!error_writer!type = file
    vserver!10!logger = combined
    vserver!10!logger!access!buffsize = 16384
    vserver!10!logger!access!filename = /var/log/cherokee/cherokee.access
    vserver!10!logger!access!type = file
    vserver!10!nick = default
    vserver!10!rule!5!encoder!gzip = allow
    vserver!10!rule!5!handler = server_info
    vserver!10!rule!5!handler!type = just_about
    vserver!10!rule!5!match = directory
    vserver!10!rule!5!match!directory = /about
    vserver!10!rule!4!document_root = /usr/lib/cgi-bin
    vserver!10!rule!4!handler = cgi
    vserver!10!rule!4!match = directory
    vserver!10!rule!4!match!directory = /cgi-bin
    vserver!10!rule!3!document_root = /usr/share/cherokee/themes
    vserver!10!rule!3!handler = file
    vserver!10!rule!3!match = directory
    vserver!10!rule!3!match!directory = /cherokee_themes
    vserver!10!rule!2!document_root = /usr/share/cherokee/icons
    vserver!10!rule!2!handler = file
    vserver!10!rule!2!match = directory
    vserver!10!rule!2!match!directory = /icons
    vserver!10!rule!1!handler = common
    vserver!10!rule!1!handler!iocache = 1
    vserver!10!rule!1!match = default
    vserver!20!document_root =
    /home/mz/generador_valores/web/app/generador/static
    vserver!20!error_writer!filename = /var/log/cherokee/cherokee.error
    vserver!20!error_writer!type = file
    vserver!20!logger = combined
    vserver!20!logger!access!buffsize = 16384
    vserver!20!logger!access!filename = /var/log/cherokee/cherokee.access
    vserver!20!logger!access!type = file
    vserver!20!nick = generador.local.lab
    vserver!20!rule!30!encoder!deflate = 0
    vserver!20!rule!30!encoder!gzip = 0
    vserver!20!rule!30!expiration = time
    vserver!20!rule!30!expiration!time = 1h
    vserver!20!rule!30!handler = file
    vserver!20!rule!30!handler!iocache = 1
    vserver!20!rule!30!match = fullpath
    vserver!20!rule!30!match!fullpath!1 = /favicon.ico
    vserver!20!rule!30!match!fullpath!2 = /robots.txt
    vserver!20!rule!30!match!fullpath!3 = /crossdomain.xml
    vserver!20!rule!30!match!fullpath!4 = /sitemap.xml
    vserver!20!rule!30!match!fullpath!5 = /sitemap.xml.gz
    vserver!20!rule!20!document_root =
    /home/mz/generador_valores/web/app/generador/static
    vserver!20!rule!20!expiration = time
    vserver!20!rule!20!expiration!time = 7d
    vserver!20!rule!20!handler = file
    vserver!20!rule!20!match = or
    vserver!20!rule!20!match!left = directory
    vserver!20!rule!20!match!left!directory = /media
    vserver!20!rule!20!match!right = directory
    vserver!20!rule!20!match!right!directory = /static
    vserver!20!rule!10!encoder!gzip = 1
    vserver!20!rule!10!handler = scgi
    vserver!20!rule!10!handler!balancer = round_robin
    vserver!20!rule!10!handler!balancer!source!10 = 1
    vserver!20!rule!10!handler!check_file = 0
    vserver!20!rule!10!handler!error_handler = 1
    vserver!20!rule!10!match = default
    source!1!env_inherited = 1
    source!1!host = 127.0.0.1:54487
    source!1!interpreter = /home/mz/generador_valores/env/bin/python
    /home/mz/generador_valores/web/app/manage.py runfcgi protocol=scgi
    host=127.0.0.1 port=54487
    source!1!nick = Django 1
    source!1!timeout = 60
    source!1!type = interpreter



Notas
-----
* Para liberar espacio en la tarjeta SD es necesario eliminar el cache de los
  paquetes instalados. Ejecutando `pacman -Scc` se elimina todo el cache, pero
  no se pueden realizar downgrades en caso que sea necesario.
* Al realizar un upgrade del sistema via `pacman -Syu` se debe copiar de nuevo
  el archivo `/boot/uImage` del root file system a la particion FAT para que
  este lance el nuevo kernel instalado
    
