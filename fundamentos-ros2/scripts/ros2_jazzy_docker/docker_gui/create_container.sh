#!/bin/sh

# Script para criar e executar um container Docker com suporte a interface gráfica (GUI) e ROS2.
# Uso: ./create_container.sh <imagem_docker> <nome_ws_ros2> <nome_container>

DOCKER_IMAGE="$1"    # Nome da imagem Docker.
ROS2_WS_NAME="$2"     # Nome do workspace ROS2.
CONTAINER_NAME="$3"   # Nome do container a ser criado.

# Caminho para o código fonte no host (máquina física).
HOST_WS_PATH="/home/$USER/$ROS2_WS_NAME/src"

# Obtém o usuário configurado na imagem Docker.
DOCKER_USER=$(docker inspect "$DOCKER_IMAGE" --format '{{.Config.User}}')
if [ -z "$DOCKER_USER" ]; then
    DOCKER_USER="ubuntu"  # Valor padrão caso não esteja definido na imagem.
fi

# Permite conexões locais ao servidor X para interface gráfica.
xhost +local:docker

# Configurações para encaminhamento do X11.
XSOCK=/tmp/.X11-unix
XAUTH=/tmp/.docker.xauth
XAUTH_DOCKER=/tmp/.docker.xauth

# Cria o arquivo Xauth se não existir para autenticação do display.
if [ ! -f "$XAUTH" ]; then
    xauth_list=$(xauth nlist :0 | sed -e 's/^..../ffff/')
    if [ ! -z "$xauth_list" ]; then
        echo "$xauth_list" | xauth -f "$XAUTH" nmerge -
    else
        touch "$XAUTH"
    fi
    chmod a+r "$XAUTH"
fi

# Verifica a presença de GPU NVIDIA.
if nvidia-smi | grep -q NVIDIA; then
    echo "GPU NVIDIA detectada, inicializando container com suporte a GPU"
    docker run -it --network host \
        --privileged \
        --name "$CONTAINER_NAME" \
        --gpus all \
        --runtime nvidia \
        --env="DISPLAY=$DISPLAY" \
        --env="QT_X11_NO_MITSHM=1" \
        --env="NVIDIA_DRIVER_CAPABILITIES=all" \
        --volume="/etc/timezone:/etc/timezone:ro" \
        --volume="/etc/localtime:/etc/localtime:ro" \
        --volume="$XSOCK:$XSOCK:rw" \
        --volume="$XAUTH:$XAUTH_DOCKER:rw" \
        --volume="$HOST_WS_PATH:/home/$DOCKER_USER/$ROS2_WS_NAME/src" \
        "$DOCKER_IMAGE" \
        bash
else
    echo "GPU NVIDIA NÃO detectada, inicializando container sem suporte a GPU"
    docker run -it --network host \
        --privileged \
        --name "$CONTAINER_NAME" \
        --env="DISPLAY=$DISPLAY" \
        --volume="$XSOCK:$XSOCK:rw" \
        --volume="$XAUTH:$XAUTH_DOCKER:rw" \
        --volume="/dev:/dev" \
        --volume="/etc/timezone:/etc/timezone:ro" \
        --volume="/etc/localtime:/etc/localtime:ro" \
        --volume="$HOST_WS_PATH:/home/$DOCKER_USER/$ROS2_WS_NAME/src" \
        "$DOCKER_IMAGE" \
        bash
fi
