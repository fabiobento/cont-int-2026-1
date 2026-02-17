#!/usr/bin/env bash

# Para todos os containers que estão em execução no momento
echo "Parando containers em execução"
docker stop $(docker ps -q)

# Remove todos os containers que não estão sendo utilizados
echo "Deletando containers"
docker container prune

# Remove todas as imagens, containers e redes não utilizados (limpeza completa)
echo "Deletando todas as imagens"
docker system prune -a