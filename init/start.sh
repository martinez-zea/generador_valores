#! /bin/zsh

SCRIPT_CONTAINER=generador_valores #donde esta el script
SCRIPT_NAME=generador_valores.py
WHERE=`pwd` #donde estoy
GENVAL_SCRIPT=$WHERE/$SCRIPT_CONTAINER #donde esta el script

usage(){
    echo "--- genVal statrt script ---"
    echo "Uso: ./start.sh env_name"
    echo "env_name: directorio donde esta el environment"
    exit 1
}
run(){
    source $GENVAL_SCRIPT/$PYTHON_ENV/bin/activate
    cd $GENVAL_SCRIPT/generador/
    xterm -hold -e python $SCRIPT_NAME
}

if [[ $# -eq 0 ]]; then
    usage
elif [[ $# -eq 1 ]]; then
    PYTHON_ENV=$1
    if [[ -a "$PYTHON_ENV" ]]; then
        echo 'Iniciando generador de valores!!'
        run
    else
        echo 'el directorio no existe'
        usage
    fi
fi




