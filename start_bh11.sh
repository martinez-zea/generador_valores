#! /bin/zsh

#SCRIPT_CONTAINER=generador #donde esta el script
#SCRIPT_CONTAINER=/home/mz/generador_valores/generador/
#SCRIPT_NAME=generador_valores.py
#WHERE=`pwd` #donde estoy
#WHERE=/home/mz/generador_valores
#GENVAL_SCRIPT=$WHERE/$MAIN_SCRIPT #donde esta el script

#usage(){
#    echo "--- genVal statrt script ---"
#    echo "Uso: ./start.sh env_name"
#    echo "env_name: directorio donde esta el environment"
#    exit 1
#}
#run(){
#    source $WHERE/$PYTHON_ENV/bin/activate
#    cd $SCRIPT_CONTAINER
#    python $SCRIPT_NAME
#}

run(){
    xset -dpms
    xset s noblank
    xset s off
    source /home/mz/generador_valores/env/bin/activate
    cd /home/mz/generador_valores/generador
    python generador_valores.py
}

#if [[ $# -eq 0 ]]; then
#    usage
#elif [[ $# -eq 1 ]]; then
#    PYTHON_ENV=$1
#    if [[ -a "$PYTHON_ENV" ]]; then
#        echo 'Iniciando generador de valores!!'
#        run
#    else
#        echo 'el directorio no existe'
#        usage
#    fi
#fi
run
