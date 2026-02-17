#!/bin/sh

# Nome do contêiner que você criou anteriormente, executando o arquivo "create_container.sh".
CONTAINER_NAME="$1"

# Parando o contêiner existente
docker stop $CONTAINER_NAME