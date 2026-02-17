#!/usr/bin/env bash
set -e

# Configura o ambiente do ROS
source "/opt/ros/$ROS_DISTRO/setup.bash"

# Executa o comando passado como argumento
exec "$@"
