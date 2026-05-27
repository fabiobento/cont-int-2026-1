Aqui estão o roteiro e o script atualizados, incorporando as correções das dependências (`apt-get update`) e a clonagem do pacote `aws-robomaker-hospital-world` para resolver o erro do `hospital_robot_spawner`, além do comando de inicialização correto para a simulação.

### Roteiro Atualizado

# Aula 8: Roteiro Prático - Deep Reinforcement Learning para VANTs no ROS 2

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
# Adiciona o utilizador ao grupo sudo e permite o uso sem palavra-passe
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /bin/bash \
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
  -t lab_drone_rl_humble .

```

*O ponto (`.`) no final é obrigatório, ele indica que o Dockerfile está na pasta atual.*

---

### 3. Executando o Container (Run)

Para iniciar o seu novo container habilitando a Interface Gráfica e o Volume do seu workspace (nesse exemplo é `~/vant_rl_ws`):

Primeiro crie o workspace:

```bash
mkdir -p ~/vant_rl_ws/src

```

Depois, libere a interface de vídeo na máquina host:

```bash
xhost +local:root

```

Agora, inicie o container:

```bash
docker run -it --rm \
  --name drone_rl_container \
  --net=host \
  --ipc=host \
  --gpus all \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -e ROS_DOMAIN_ID=30 \
  -v ~/vant_rl_ws:/workspace \
  lab_drone_rl_humble

```

---

### 4. Concluindo a Instalação (**DENTRO DO CONTAINER**)

> **Observação:**
> Se não estiver mais no mesmo terminal em que executou o `run` acima, entre no container com o comando:
> ```bash
> docker exec -it drone_rl_container bash
> 
> ```
> 
> 

**Dentro do container**, para concluir a instalação da arquitetura do drone, crie um arquivo para o script com os seguintes comandos:

```bash
cd /workspace
touch install_drone_rl.sh
nano install_drone_rl.sh

```

Cole o código abaixo dentro desse arquivo que acabou de criar:

```bash
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
    echo 'export ROS_DOMAIN_ID=30 #DRONE_RL' >> ~/.bashrc
fi

echo "========================================================="
echo " WORKSPACE DRL CONFIGURADO E COMPILADO COM SUCESSO!"
echo " Para aplicar as mudanças no terminal atual, execute:"
echo " source ~/.bashrc"
echo "========================================================="

```

Configure a permissão de execução do script e execute-o:

```bash
chmod +x install_drone_rl.sh
./install_drone_rl.sh 

```

---

### 5. Sincronização do Código no Workspace

Como o script `install_drone_rl.sh` foi executado dentro da pasta `/workspace` (que está espelhada na sua máquina hospedeira em `~/vant_rl_ws`), o repositório `Drone-RL-Control` já foi baixado automaticamente. Qualquer modificação que você fizer nos códigos em Python ou C++ pelo seu VS Code na máquina host refletirá imediatamente dentro do container.

> **Atenção:** Durante as aulas práticas, é esperado e recomendável que vocês editem os códigos de recompensa e as observações do RL para testar novas hipóteses de desvio de obstáculos.

---

### 6. Iniciando a simulação (**DENTRO DO CONTAINER**)

> **Observação**
> Os comandos daqui em diante serão executados **DENTRO DO CONTAINER**.

Para carregar os pacotes compilados e iniciar o ambiente simulado do hospital com o modelo do drone:

```bash
source /workspace/install/setup.bash
ros2 launch drone_rl drone_rl_start.launch.py

```

---

### 7. Inicie o Treinamento DRL

Abra um segundo terminal e entre no container para rodar a rotina de treinamento:

```bash
docker exec -it drone_rl_container bash
source /workspace/install/setup.bash

```

Execute o nó de treinamento por Aprendizado por Reforço (PPO/SAC):

```bash
ros2 run drone_rl train_rl_model

```

---

### 8. Registre e Monitore os Dados do Treinamento

Abra um terceiro terminal e entre no container. Para visualizar as métricas de recompensa e perdas (loss) em tempo real via Tensorboard:

```bash
docker exec -it drone_rl_container bash
source /workspace/install/setup.bash

```

Inicie o servidor do Tensorboard apontando para o diretório de logs:

```bash
tensorboard --logdir ./logs/

```

*(Acesse o link `http://localhost:6006` gerado no terminal usando o navegador da sua máquina física).*

---

### 9. Teste o modelo treinado (Inferência)

Abra um quarto terminal e entre no container:

```bash
docker exec -it drone_rl_container bash
source /workspace/install/setup.bash

```

Verifique se o arquivo resultante do modelo foi salvo com sucesso (geralmente `.zip` gerado pela Stable Baselines3):

```bash
ls -l /workspace/src/Drone-RL-Control/models/

```

Se o arquivo foi criado, inicie a inferência para ver o drone navegando autonomamente de forma reativa:

```bash
ros2 run drone_rl test_rl_model

```

---
