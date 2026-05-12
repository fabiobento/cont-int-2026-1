# Aula 7: Deep Reinforcement Learning no ROS 2

### 1. Crie o arquivo Dockerfile

No seu terminal físico, crie uma pasta para guardar as configurações do Docker e crie o arquivo:

```bash
mkdir -p ~/docker_ros2
cd ~/docker_ros2
nano Dockerfile
```

Cole o conteúdo abaixo dentro do arquivo:

```dockerfile
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
    ros-humble-turtlebot3-teleop \
    ros-humble-turtlebot3-description \
    ros-humble-turtlebot3-gazebo \
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
```

*(Salve apertando `Ctrl+O`, `Enter`, e saia com `Ctrl+X`).*

---

### 2. Construindo a Imagem (Build)

Agora, vamos transformar esse `Dockerfile` em uma imagem real na sua máquina. Execute o comando abaixo na mesma pasta onde você salvou o arquivo `Dockerfile`. Vamos usar comandos do próprio Ubuntu `(id -u e id -g)` para ler qual é a sua numeração exata no sistema e passar isso para dentro do Docker: 

```bash
docker build \
  --build-arg USER_UID=$(id -u) \
  --build-arg USER_GID=$(id -g) \
  -t lab_ros2_humble .

```

*O ponto (`.`) no final é obrigatório, ele indica que o Dockerfile está na pasta atual.*

---

### 3. Executando o Container (Run)

Para iniciar o seu novo container habilitando a Interface Gráfica, o Volume do seu workspace (`~/turtlebot3_ws`) e a **GPU (se presente)**, a estrutura do comando será a seguinte:

Primeiro, libere a interface de vídeo na máquina host:

```bash
xhost +local:root

```

Agora, inicie o container:

```bash
docker run -it --rm \
  --name humble_gpu_container \
  --net=host \
  --ipc=host \
  --gpus all \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -e ROS_DOMAIN_ID=30 \
  -v ~/turtlebot3_ws:/workspace \
  lab_ros2_humble
```
### 4. Concluindo a Instalação(dentro do container)
Para concluir a instalação, crie um arquivo para o script com os seguintes comandos:
```bash
cd /workspace
touch install_tb3_humble.sh
nano install_tb3_humble.sh
```
Cole o código abaixo dentro desse arquivo que acabou de criar:
```bash
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
```