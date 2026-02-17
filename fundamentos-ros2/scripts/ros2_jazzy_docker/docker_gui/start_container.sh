#!/bin/sh

# Nome do container criado anteriormente através do script "create_container.sh".
CONTAINER_NAME="$1"

# Habilita o controle de acesso para o servidor X para evitar problemas com a interface gráfica (GUI).
xhost +local:docker

XSOCK=/tmp/.X11-unix
XAUTH=/tmp/.docker.xauth
XAUTH_DOCKER=/tmp/.docker.xauth

# Cria o arquivo Xauth caso ele não exista para autenticação do X11.
if [ ! -f $XAUTH ]; then
    xauth_list=$(xauth nlist :0 | sed -e 's/^..../ffff/')
    if [ ! -z "$xauth_list" ]; then
        echo "$xauth_list" | xauth -f $XAUTH nmerge -
    else
        touch $XAUTH
    fi
    chmod a+r $XAUTH
fi

# Inicia o container e abre um terminal interativo bash.
docker start $CONTAINER_NAME 
docker exec -it $CONTAINER_NAME bash  