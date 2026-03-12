#!/bin/bash

CONTAINER_NAME="$1"

if [ -z "$CONTAINER_NAME" ]; then
    echo "Uso: ./start_container.sh nome_do_container"
    exit 1
fi

# 1. Libera acesso ao X
xhost +local:docker

XAUTH=/tmp/.docker.xauth

# 2. Força a recriação do arquivo como FILE (não diretório)
# Remove se existir para evitar o erro de "not a directory"
sudo rm -rf $XAUTH
touch $XAUTH

# 3. Gera os tokens de autorização
xauth_list=$(xauth nlist $DISPLAY | sed -e 's/^..../ffff/')
if [ ! -z "$xauth_list" ]; then
    echo "$xauth_list" | xauth -f $XAUTH nmerge -
fi

# 4. Ajusta permissões para o Docker conseguir ler
chmod 777 $XAUTH

# 5. Inicia o container
docker start $CONTAINER_NAME

# 6. Entra no container
docker exec -it $CONTAINER_NAME bash