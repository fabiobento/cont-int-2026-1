#!/bin/sh

# Nome do container que você criou anteriormente, executando o arquivo "create_container.sh".
CONTAINER_NAME="$1"

# Parando e removendo o container existente
docker stop $CONTAINER_NAME
docker rm $CONTAINER_NAME
