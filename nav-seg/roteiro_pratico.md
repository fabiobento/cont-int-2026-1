

# Projeto Final - Navegação Reativa e Coordenação de Frotas de Robôs Terrestres (Líder-Seguidor)

Este guia orienta a construção da imagem Docker, configuração do ecossistema ROS 2 Humble / Gazebo e a correta exportação de telas em ambientes locais ou remotos (via SSH).

---

## 1. Construção da Imagem Docker

### 1.1. Crie o arquivo Dockerfile

No seu terminal, crie uma pasta para organizar as configurações do Docker e crie o arquivo:

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
    ros-humble-ros-gz \
    ros-humble-ign-ros2-control \
    && rm -rf /var/lib/apt/lists/*

# ====================================================================
# INSTALAÇÃO DE BIBLIOTECAS DE INTELIGÊNCIA ARTIFICIAL (DRL)
# ====================================================================
RUN pip3 install 'numpy<2' gymnasium stable-baselines3[extra]

# ====================================================================
# CONFIGURAÇÃO DE USUÁRIO NÃO-ROOT
# ====================================================================
ARG USERNAME=robot
ARG USER_UID=1000
ARG USER_GID=1000

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /bin/bash \
    && usermod -aG sudo $USERNAME \
    && echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# ====================================================================
# SUPORTE A GPU (NVIDIA) E INTERFACE GRÁFICA
# ====================================================================
ENV NVIDIA_VISIBLE_DEVICES ${NVIDIA_VISIBLE_DEVICES:-all}
ENV NVIDIA_DRIVER_CAPABILITIES ${NVIDIA_DRIVER_CAPABILITIES:+$NVIDIA_DRIVER_CAPABILITIES,}graphics,display,video,utility
ENV QT_X11_NO_MITSHM=1

# Variável de domínio da rede do laboratório
ENV ROS_DOMAIN_ID=30

# ====================================================================
# CONFIGURAÇÃO DO WORKSPACE
# ====================================================================
WORKDIR /workspace
RUN chown -R $USER_UID:$USER_GID /workspace

USER $USERNAME

RUN echo "source /opt/ros/humble/setup.bash" >> /home/$USERNAME/.bashrc \
    && echo "source /usr/share/gazebo/setup.sh" >> /home/$USERNAME/.bashrc

CMD ["bash"]

```

*(Salve apertando `Ctrl+O`, `Enter`, e saia com `Ctrl+X`).*

### 1.2. Construindo a Imagem (Build)

Execute o comando de build mapeando o UID e GID do seu usuário para evitar conflitos de permissões em volumes compartilhados:

```bash
docker build \
  --build-arg USER_UID=$(id -u) \
  --build-arg USER_GID=$(id -g) \
  -t ros2_humble .

```

---

## 2. Preparação do Servidor Gráfico (X11)

Antes de iniciar o container, você deve preparar a autorização visual dependendo de onde está acessando a máquina do laboratório:

### Opção A: Acesso Direto (Máquina Física/Local)

Se você está sentado em frente ao computador do laboratório, basta rodar:

```bash
xhost +local:root

```

### Opção B: Acesso Remoto (Via SSH com X11 Forwarding)

Se você acessou a máquina via `ssh -X usuario@servidor`, o comando `xhost` falhará. Use o método de cookies de autenticação do `xauth`:

```bash
# 1. Verifique o ID do display criado pelo SSH
echo $DISPLAY
# Exemplo de saída: localhost:12.0

# 2. Extraia o cookie do display correspondente (troque o '12' pelo número retornado acima)
mkdir -p ~/tmp
xauth extract ~/tmp/xauth_docker localhost:12

# 3. Permita que o container leia o arquivo de cookie
chmod 644 ~/tmp/xauth_docker

```

---

## 3. Executando o Container (Run)

Prepare a pasta do seu Workspace na máquina host:

```bash
mkdir -p ~/lab_ros_ws/src

```

Inicie o container injetando os parâmetros de rede, aceleração de hardware e as configurações visuais apropriadas:

```bash
docker run -it --rm \
  --name humble_gpu_container \
  --net=host \
  --ipc=host \
  --gpus all \
  -e DISPLAY=$DISPLAY \
  -v ~/tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v ~/tmp/xauth_docker:/tmp/.xauth_docker:ro \
  -e XAUTHORITY=/tmp/.xauth_docker \
  -e ROS_DOMAIN_ID=30 \
  -v ~/lab_ros_ws:/workspace \
  ros2_humble

```

> *Nota: Se estiver usando o acesso local (Opção A), as flags `-v ~/tmp/xauth_docker` e `-e XAUTHORITY` podem ser omitidas sem problemas.*

---

## 4. Concluindo a Instalação (Dentro do Container)

> ⚠️ **IMPORTANTE:** A partir deste ponto, todas as operações são executadas **DENTRO** do container.

Para validar se o X11 Forwarding funcionou, faça um teste rápido:

```bash
xclock

```

*Se uma janela de relógio analógico abrir na sua tela, a interface gráfica está funcionando.*

Agora, configure o ecossistema do TurtleBot3:

```bash
cd /workspace
touch install_tb3_humble.sh
nano install_tb3_humble.sh

```

Cole o script de automação abaixo:

```bash
#!/bin/bash
set -e 

echo "[1/5] Preparando o Workspace..."
source /opt/ros/humble/setup.bash
mkdir -p /workspace/src
cd /workspace/src/

echo "[2/5] Clonando repositórios do TurtleBot3..."
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
if ! grep -q "/workspace/install/setup.bash" ~/.bashrc; then
    echo "" >> ~/.bashrc
    echo "# ===================================================" >> ~/.bashrc
    echo "# Configurações TurtleBot3 - ROS 2 Humble" >> ~/.bashrc
    echo "# ===================================================" >> ~/.bashrc
    echo 'source /workspace/install/setup.bash' >> ~/.bashrc
    echo 'export TURTLEBOT3_MODEL=burger' >> ~/.bashrc
    echo 'export ROS_DOMAIN_ID=0 #TURTLEBOT3' >> ~/.bashrc
fi

echo "========================================================="
echo " WORKSPACE CONFIGURADO E COMPILADO COM SUCESSO!"
echo " Execute: source ~/.bashrc"
echo "========================================================="

```

Dê permissão e execute o script:

```bash
chmod +x install_tb3_humble.sh
./install_tb3_humble.sh
source ~/.bashrc

```

---

## 5. Simulação do Seguidor (*Follower*)

### 5.1. Descrição do Exemplo

Este pacote demonstra uma técnica de navegação em frota estilo líder-seguidor. O robô da frente (líder) é controlado manualmente e os subsequentes utilizam dados de odometria combinados com o planejador local do `Nav2` para segui-lo em fila.

> ℹ️ **Observação:** O desvio acumulado na odometria (*drift*) pode reduzir a precisão do alinhamento ao longo do tempo.

Você pode conferir o comportamento dinâmico esperado neste link: **[Vídeo de execução do seguidor](https://www.youtube.com/watch?v=YXF3FeRNSeE)**.

### 5.2. Abertura de Múltiplos Terminais (**Modo Operacional**)

Sempre que o roteiro exigir novos terminais durante os testes de simulação, abra uma nova aba na sua máquina host e acesse o container com:

```bash
docker exec -it humble_gpu_container bash
source ~/.bashrc

```

### 5.3 Carregando Múltiplos TurtleBot3s

#### 5.3.1 Descrição

> Esse vídeo ilustra o controle de multiplos TurtleBot3 simultanemante: [TurtleBot3 Example: Multi-Robot Control](https://www.youtube.com/watch?v=IVut8qZOrEk&t=40s).

Nessa ubseção vamos aprender como operar múltiplos TurtleBot3s a partir de um único PC Remoto.
Se você operar vários TurtleBots como se estivesse operando apenas um, não conseguirá distinguir qual tópico pertence a qual robô.
![]()