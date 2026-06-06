# Usa a imagem oficial do ROS 2 Humble
FROM osrf/ros:humble-desktop

ENV DEBIAN_FRONTEND=noninteractive

# Instala ferramentas essenciais, 'sudo' e todas as dependências do ROS/Gazebo
RUN apt-get update && apt-get install -y \
    nano \
    git \
    wget \
    curl \
    python3-pip \
    python3-rosdep \
    mesa-utils \
    libgl1-mesa-glx \
    x11-apps \
    sudo \
    python3-colcon-common-extensions \
    ros-humble-gazebo-* \
    ros-humble-cartographer \
    ros-humble-cartographer-ros \
    ros-humble-navigation2 \
    ros-humble-nav2-bringup \
    ros-humble-ros-gz \
    ros-humble-ign-ros2-control \
    && rm -rf /var/lib/apt/lists/*



# ====================================================================
# INSTALAÇÃO DE BIBLIOTECAS DE INTELIGÊNCIA ARTIFICIAL (DRL)
# ====================================================================
# Instalado globalmente na imagem. O numpy<2 garante estabilidade com ROS/Gym.
RUN pip3 install 'numpy<2' gymnasium stable-baselines3[extra]

# ====================================================================
# CONFIGURAÇÃO DE USUÁRIO NÃO-ROOT
# ====================================================================
# Argumentos que receberão os IDs da sua máquina host durante o build
ARG USERNAME=robot
ARG USER_UID=1000
ARG USER_GID=1000

# Cria o grupo e o utilizador com os IDs exatos da máquina física
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /bin/bash \
    # Adiciona o utilizador ao grupo sudo e permite o uso sem palavra-passe
    && usermod -aG sudo $USERNAME \
    && echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# ====================================================================
# SUPORTE A GPU (NVIDIA) E INTERFACE GRÁFICA
# ====================================================================
ENV NVIDIA_VISIBLE_DEVICES \
    ${NVIDIA_VISIBLE_DEVICES:-all}
ENV NVIDIA_DRIVER_CAPABILITIES \
    ${NVIDIA_DRIVER_CAPABILITIES:+$NVIDIA_DRIVER_CAPABILITIES,}graphics,display,video,utility
ENV QT_X11_NO_MITSHM=1

# Variável de domínio da rede do laboratório
ENV ROS_DOMAIN_ID=30

# ====================================================================
# CONFIGURAÇÃO DO WORKSPACE
# ====================================================================
WORKDIR /workspace

# Muda o dono da pasta inicial para o novo utilizador
RUN chown -R $USER_UID:$USER_GID /workspace

# Muda efetivamente do 'root' para o utilizador definido
USER $USERNAME

# Adiciona os 'sources' base no terminal do novo utilizador
RUN echo "source /opt/ros/humble/setup.bash" >> /home/$USERNAME/.bashrc \
    && echo "source /usr/share/gazebo/setup.sh" >> /home/$USERNAME/.bashrc

CMD ["bash"]