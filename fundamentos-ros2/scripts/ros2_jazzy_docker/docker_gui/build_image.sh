#!/bin/bash
# Este script serve para criar uma imagem docker a partir do Dockerfile.

# Define o nome da imagem como uma variável aqui
IMAGE_NAME="$1"  # Configurando o nome da imagem como argumento
ROS_WS="$2"      # Configurando o nome da pasta do workspace ROS do PC host
USER_NAME="$3"   # Atribuindo o nome de usuário host ao docker  


# Constrói a imagem Docker com o nome de imagem especificado
docker build -f Dockerfile.master_ros2 -t "$IMAGE_NAME" . --build-arg docker_user_name="$USER_NAME" --build-arg ros_ws="$ROS_WS"
