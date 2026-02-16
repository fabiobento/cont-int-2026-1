#!/bin/bash -eu

# The BSD License
# Copyright (c) 2024 RUNTIME Robotics

#set -x

echo "################################################################"
echo ""
echo ">>> {Desinstalando a instalação do ROS Jazzy do seu computador}"
echo ""
echo ">>> {Levará alguns minutos para concluir}"
echo ""
sudo apt purge -y ros-jazzy-*
echo ""
echo "#################################################################"
echo ""
echo ">>> {Removendo automaticamente pacotes dependentes}"
sudo apt -y autoremove
echo ""
echo ">>> {Concluído: Desinstalação do ROS Jazzy}"
echo "#################################################################"
