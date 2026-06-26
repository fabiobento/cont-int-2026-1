#!/bin/bash

# =================================================================
# Script de Configuração TurtleBot3 - ROS 2 Humble
# Disciplina: Controle Inteligente - Prof. Fabio
# =================================================================

set -e # Interrompe o script se algum comando falhar

echo "[1/5] Preparando o Workspace..."
# Garante que o ambiente base do ROS Humble está carregado para a compilação
source /opt/ros/humble/setup.bash

mkdir -p /workspace/src
cd /workspace/src/

echo "[2/5] Clonando repositórios do TurtleBot3 (Branch: humble)..."
# Utiliza a branch oficial da Robotis para a versão Humble (sem o sufixo -devel)
git clone -b humble https://github.com/ROBOTIS-GIT/DynamixelSDK.git || true
git clone -b humble https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git || true
git clone -b humble https://github.com/ROBOTIS-GIT/turtlebot3.git || true
git clone -b humble https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git || true
git clone -b humble https://github.com/ROBOTIS-GIT/turtlebot3_applications.git || true
git clone -b humble https://github.com/ROBOTIS-GIT/turtlebot3_applications_msgs.git || true


echo "[3/5] Instalando dependências do ROS (rosdep)..."
cd /workspace
sudo apt-get update
sudo rosdep init || true
rosdep update
rosdep install --from-paths src --ignore-src -r -y

echo "[4/5] Compilando o Workspace com Colcon..."
colcon build --symlink-install

echo "[5/5] Configurando variáveis de ambiente adicionais no .bashrc..."
# Adiciona as variáveis do utilizador ao bashrc se ainda não existirem
if ! grep -q "/workspace/install/setup.bash" ~/.bashrc; then
    echo "" >> ~/.bashrc
    echo "# ===================================================" >> ~/.bashrc
    echo "# Configurações TurtleBot3 - ROS 2 Humble" >> ~/.bashrc
    echo "# ===================================================" >> ~/.bashrc
echo 'source /workspace/install/setup.bash' >> ~/.bashrc
    # A variável TURTLEBOT3_MODEL e ROS_DOMAIN_ID agora são gerenciadas nativamente pelo Docker
fi

echo "========================================================="
echo " WORKSPACE CONFIGURADO E COMPILADO COM SUCESSO!"
echo " Para aplicar as mudanças no terminal atual, execute:"
echo " source ~/.bashrc"
echo "========================================================="