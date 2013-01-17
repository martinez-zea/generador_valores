#! /bin/zsh

SCRIPT_CONTAINER=/home/mz/generador_valores #donde esta el script
SCRIPT_NAME=generador_valores.py

usage(){
    xset -dpms
    xset s noblank
    xset s off
    echo "--- genVal statrt script ---"
    echo "Uso: ./start.sh env_name"
    echo "env_name: directorio donde esta el environment"
    exit 1
}
run(){
    source $SCRIPT_CONTAINER/env/bin/activate
    cd $SCRIPT_CONTAINER/generador/
    python $SCRIPT_NAME
}

run




