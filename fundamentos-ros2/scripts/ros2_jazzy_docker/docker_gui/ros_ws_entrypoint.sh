#!/usr/bin/env bash
set -e

# Carrega o ambiente global do ROS 2 Jazzy
source "/opt/ros/jazzy/setup.bash"

# Carrega o workspace local se ele existir
if [ -f "$ROS_WS/install/setup.bash" ]; then
  source "$ROS_WS/install/setup.bash"
fi

exec "$@"