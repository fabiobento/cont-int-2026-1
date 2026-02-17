#!/usr/bin/env bash
set -e

# Configura o ambiente do workspace ROS
source "$ROS_WS/install/setup.bash"

# Executa o comando fornecido como argumento (mantendo o PID 1 no container)
exec "$@"
