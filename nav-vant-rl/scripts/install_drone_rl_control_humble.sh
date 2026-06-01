#!/bin/bash

# =================================================================
# Script de Configuração Drone-RL-Control - ROS 2 Humble
# Disciplina: Controle Inteligente
# =================================================================

set -e # Interrompe o script se algum comando falhar

echo "[1/5] Preparando o Workspace..."
# Garante que o ambiente base do ROS Humble está carregado para a compilação
source /opt/ros/humble/setup.bash

mkdir -p /workspace/src
cd /workspace/src/

echo "[2/5] Clonando repositórios do projeto Drone-RL-Control e dependências..."
# Clona o repositório principal de controle por Aprendizado por Reforço
git clone https://github.com/melaniayoo/Drone-RL-Control.git || true

# Clona o pacote do AWS Hospital World (branch ros2) exigido para lançar o cenário
git clone -b ros2 https://github.com/aws-robotics/aws-robomaker-hospital-world.git || true

echo "[3/5] Instalando dependências do ROS (rosdep)..."
cd /workspace
sudo apt-get update # Garante que as listas de pacotes estão atualizadas
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
    echo "# Configurações Drone-RL-Control - ROS 2 Humble" >> ~/.bashrc
    echo "# ===================================================" >> ~/.bashrc
    echo 'source /workspace/install/setup.bash' >> ~/.bashrc
    echo 'export ROS_DOMAIN_ID=0 #DRONE_RL' >> ~/.bashrc
fi

echo "========================================================="
echo " WORKSPACE DRL CONFIGURADO E COMPILADO COM SUCESSO!"
echo " Para aplicar as mudanças no terminal atual, execute:"
echo " source ~/.bashrc"
echo "========================================================="