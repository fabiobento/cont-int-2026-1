#!/bin/bash

# =================================================================
# Script de Configuração TurtleBot3 - ROS 2 Humble
# Disciplina: Controle Inteligente - Prof. Fabio
# =================================================================

set -e # Interrompe o script se algum comando falhar

echo "[1/4] Preparando o Workspace..."
# Garante que o ambiente base do ROS Humble está carregado para a compilação
source /opt/ros/humble/setup.bash

mkdir -p /workspace/src
cd /workspace/src/

echo "[2/4] Clonando repositórios do TurtleBot3 (Branch: humble-devel)..."
# Utiliza a branch oficial da Robotis para a versão Humble
git clone -b humble-devel https://github.com/ROBOTIS-GIT/DynamixelSDK.git || true
git clone -b humble-devel https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git || true
git clone -b humble-devel https://github.com/ROBOTIS-GIT/turtlebot3.git || true
git clone -b humble-devel https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git || true

echo "[3/4] Compilando o Workspace com Colcon..."
cd /workspace
colcon build --symlink-install

echo "[4/4] Configurando variáveis de ambiente adicionais no .bashrc..."
# Adiciona as variáveis do utilizador ao bashrc se ainda não existirem
if ! grep -q "/workspace/install/setup.bash" ~/.bashrc; then
    echo "" >> ~/.bashrc
    echo "# ===================================================" >> ~/.bashrc
    echo "# Configurações TurtleBot3 - ROS 2 Humble" >> ~/.bashrc
    echo "# ===================================================" >> ~/.bashrc
    echo 'source /workspace/install/setup.bash' >> ~/.bashrc
    echo 'export TURTLEBOT3_MODEL=waffle' >> ~/.bashrc
    echo 'export ROS_DOMAIN_ID=30 #TURTLEBOT3' >> ~/.bashrc
fi

echo "========================================================="
echo " WORKSPACE CONFIGURADO E COMPILADO COM SUCESSO!"
echo " Para aplicar as mudanças no terminal atual, execute:"
echo " source ~/.bashrc"
echo "========================================================="
```

Configure a permissão de execução do script e execute-o:
```bash
chmod +x install_tb3_humble.sh
./install_tb3_humble.sh 