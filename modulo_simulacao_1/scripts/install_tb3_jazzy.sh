#!/bin/bash

# =================================================================
# Script de Instalação TurtleBot3 - ROS 2 Jazzy (Ubuntu 24.04)
# =================================================================

set -e # Interrompe o script se algum comando falhar

echo "[1/5] Atualizando sistema e instalando dependências do Gazebo..."
sudo apt-get update
sudo apt-get install -y curl lsb-release gnupg

# Configuração do repositório oficial do Gazebo (OSRF)
sudo curl https://packages.osrfoundation.org/gazebo.gpg --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null

sudo apt-get update
sudo apt-get install -y gz-harmonic

echo "[2/5] Instalando pacotes de Navegação e SLAM (Cartographer/Nav2)..."
sudo apt install -y ros-jazzy-cartographer \
                    ros-jazzy-cartographer-ros \
                    ros-jazzy-navigation2 \
                    ros-jazzy-nav2-bringup \
                    python3-colcon-common-extensions

echo "[3/5] Criando Workspace e clonando repositórios do TurtleBot3..."
# Garante que o ambiente base do ROS Jazzy está carregado para a compilação
source /opt/ros/jazzy/setup.bash

mkdir -p ~/turtlebot3_ws/src
cd ~/turtlebot3_ws/src/

# Clonando branches específicas para Jazzy
git clone -b jazzy https://github.com/ROBOTIS-GIT/DynamixelSDK.git
git clone -b jazzy https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git
git clone -b jazzy https://github.com/ROBOTIS-GIT/turtlebot3.git

echo "[4/5] Compilando o Workspace com Colcon..."
cd ~/turtlebot3_ws
colcon build --symlink-install

echo "[5/5] Configurando variáveis de ambiente no .bashrc..."
# Evitar duplicatas no .bashrc se o script for rodado duas vezes
if ! grep -q "turtlebot3_ws/install/setup.bash" ~/.bashrc; then
    echo 'source /opt/ros/jazzy/setup.bash' >> ~/.bashrc
    echo 'source ~/turtlebot3_ws/install/setup.bash' >> ~/.bashrc
    echo 'export ROS_DOMAIN_ID=30' >> ~/.bashrc
    echo 'export TURTLEBOT3_MODEL=waffle' >> ~/.bashrc
fi

echo "========================================================="
echo " INSTALAÇÃO CONCLUÍDA COM SUCESSO!"
echo " Por favor, feche este terminal e abra um novo ou execute:"
echo " source ~/.bashrc"
echo "========================================================="