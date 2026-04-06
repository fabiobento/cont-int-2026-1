# Aula 4 : Simulação e Inspeção de Dados no ROS 2 Jazzy

## 1. Objetivos
* Configurar o ambiente para o **TurtleBot3 Waffle** no Ubuntu 24.04.
* Lançar o mundo de simulação no Gazebo e inspecionar a física.
* Utilizar ferramentas de diagnóstico (`rqt_graph` e `ros2 topic`).
* Configurar o **RViz2** manualmente para visualização de sensores (LiDAR e Odometria).

---
## 2. Isolamento de Rede no Laboratório (Obrigatório)

Como estamos todos conectados à mesma rede Wi-Fi, o ROS 2 tentará conectar os nós de todos os computadores automaticamente. Se não isolarmos a rede, o seu controlador tentará mover o robô do colega ao lado!

Para evitar isso, cada aluno receberá um número de identificação (ID) único  correspondente a sua bancada.

Abra o terminal e verifique se a variável de ambiente `ROS_DOMAIN_ID` está vazia:
```bash
echo $ROS_DOMAIN_ID
```

Caso esteja vazia ou não esteja com o número de sua bancada, abra o Terminal e exporte a variável ambiental `ROS_DOMAIN_ID` **antes** de rodar qualquer comando ROS 2 da seguinte forma:

1. Adicione o comando ao final do arquivo `.bashrc` (substitua XX pelo número de sua bancada, ex: export ROS_DOMAIN_ID=7)
    ```bash
    echo "export ROS_DOMAIN_ID=XX" >> ~/.bashrc
    ```

2. Recarregue as configurações para aplicar no terminal atual
    ```bash
    source ~/.bashrc

---
## 3. Preparando o Ambiente: Obtendo o Código da Disciplina

Para realizarmos as práticas de ROS 2, você precisará dos scripts, *packages* e arquivos de configuração mais recentes. Todo o material é atualizado constantemente no repositório da disciplina no GitHub.

Siga as instruções abaixo de acordo com a sua situação no laboratório de hoje:

**1. Primeira vez usando o repositório (Ainda não baixou)**
Se você está usando um computador novo no laboratório ou ainda não baixou o material deste semestre, abra o Terminal e execute o comando de clonagem para trazer o projeto para a sua máquina:

```bash
cd
git clone https://github.com/fabiobento/cont-int-2026-1.git
```

**2. Atualizando o repositório existente (Já baixou anteriormente)**
Se você já tem a pasta do projeto no seu computador, precisaremos sincronizá-la com as atualizações da semana.

> **Atenção:** Durante as aulas práticas, é esperado e recomendável que vocês editem os códigos para testar hipóteses. No entanto, para iniciar a aula de hoje sem erros de conflito, usaremos uma sequência de comandos que baixa as novidades e **sobrescreve** qualquer alteração local. Isso garante que o seu ambiente fique exatamente igual à versão oficial para o roteiro de hoje.

Abra o Terminal e execute a seguinte sequência:

```bash
cd ~/cont-int-2026-1
git fetch
git reset --hard origin/main
```

**O que esses comandos fazem?**

* **`cd cont-int-2026-1`**: Garante que você está dentro da pasta correta do projeto.
* **`git fetch`**: Consulta o GitHub e baixa silenciosamente as informações mais recentes do servidor, mas ainda não altera os seus arquivos visíveis.
* **`git reset --hard origin/master`**: Força os seus arquivos locais a ficarem idênticos à ramificação principal (`master`) oficial, descartando testes e modificações residuais das aulas anteriores.
## 4. Configuração do Ambiente

Antes de iniciar, precisamos garantir que as variáveis de ambiente e os pacotes necessários estejam instalados. Execute no terminal:

```bash
# Instalação das dependências do TurtleBot3 para Jazzy
sudo apt update
sudo apt install ros-jazzy-turtlebot3 ros-jazzy-turtlebot3-gazebo
sudo apt install ros-jazzy-turtlebot3-simulations ros-jazzy-turtlebot3-description

# Definição do modelo do robô (adicione ao seu .bashrc para persistência)
export TURTLEBOT3_MODEL=waffle
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:/opt/ros/jazzy/share/turtlebot3_gazebo/models

## Baixar e compilar o repositório do Turtlebot3
cd ~/master_ros2_ws/src/
git clone -b jazzy https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git
cd ~/master_ros2_ws && colcon build --symlink-install
source install/setup.bash
```

---

## 5. Lançando a Simulação
Este comando inicializa o motor de física Gazebo, carrega o mundo de obstáculos e o nó `robot_state_publisher` que gerencia a árvore de transformadas (TF).

```bash
ros2 launch turtlebot3_gazebo turtlebot3_empty.launch.py
```
> **Dica:** O Gazebo pode demorar um pouco no primeiro carregamento para baixar os modelos. Aguarde até ver o robô posicionado no centro do mapa.

---

## 6. Inspeção do Grafo e Fluxo de Dados
Abra um **novo terminal** e utilize as ferramentas de introspecção do ROS 2:

1.  **Grafo de Nós:** `rqt_graph`
    * Observe como o nó `/gazebo` se comunica com os demais.
2.  **Lista de Tópicos:** `ros2 topic list`
    * Verifique a existência dos tópicos `/cmd_vel`, `/odom`, `/scan` e `/tf`.
3.  **Frequência de Atualização:** Escolha o tópico do laser e verifique a taxa de publicação:
    ```bash
    ros2 topic hz /scan
    ```

---

## 7. Visualização Avançada no RViz2
O RViz2 é essencial para depurar o que o robô "vê". Ele inicia vazio, e você deve configurá-lo manualmente:

1.  No terminal, digite: `rviz2`
2.  No painel **Global Options**, altere o **Fixed Frame** para `odom`.
3.  Clique em **Add** e na aba **By display type**$\rightarrow$**rviz_default_plugins** adicione os seguintes displays:
    * **RobotModel**: Renderiza o Waffle em 3D.
    * **TF**: Mostra os eixos coordenados. Na opção **TF**$\rightarrow$**Frames** habilite os frames `base_link` e `odom`.
    * **LaserScan**: Na aba **By topic** selecione o tópico  `/scan`$\rightarrow$`LaserScan`. (Sugestão: mude o *Style* para `Points` e *Size* para `0.03` pixels).
    * **Odometry**: Na aba **By topic** selecione o tópico selecione o tópico `/odom`$\rightarrow$`Odometry`. Isso mostrará o rastro do robô.



---

## 8. Implementação: Controle de Malha Aberta (Python)
**Crie um pacote** Python chamado `controle_simulacao` conforme você aprendeu na seção ["*Criando um pacote Python*" da "*Aula 2: Escrevendo e Construindo um Nó ROS 2*"](https://github.com/fabiobento/cont-int-2026-1/blob/main/nodes-ros2/nodes-ros2.md#criando-um-pacote-python). 

Em seguida, **crie o nó Python**, conforme você estudo em na seção [*Criando um nó em Python* da *"Aula 2: Escrevendo e Construindo um Nó ROS 2"*](https://github.com/fabiobento/cont-int-2026-1/blob/main/nodes-ros2/nodes-ros2.md#criando-um-n%C3%B3-em-python). Para implementar nó use o código abaixo e salve o arquivo como `circulo.py`. O objetivo é aplicar a **Cinemática Direta** para realizar uma trajetória circular.

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class CircularMotion(Node):
    def __init__(self):
        super().__init__('circular_motion_node')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        timer_period = 0.1  # 10 Hz
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.get_logger().info('Executando trajetória circular...')

    def timer_callback(self):
        msg = Twist()
        # v = 0.15 m/s | w = 0.4 rad/s
        msg.linear.x = 0.15
        msg.angular.z = 0.4
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = CircularMotion()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Comando de parada enviado.')
        node.publisher_.publish(Twist()) # Stop
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

Agora configure o arquivo `setup.py` do pacote `controle_simulacao` para que o nó `circulo.py` seja **executável no ROS2**.
```python
from setuptools import find_packages, setup

package_name = 'controle_simulacao'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='nome',
    maintainer_email='email@email.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        'circulo = controle_simulacao.circulo:main',
        ],
    },
)
```

Agora **adicione as dependências** do pacote `controle_simulacao` no arquivo `package.xml`.
```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>controle_simulacao</name>
  <version>0.0.0</version>
  <description>TODO: Package description</description>
  <maintainer email="fabio.obento@gmail.com">fabio</maintainer>
  <license>TODO: License declaration</license>

  <depend>rclpy</depend>
  <depend>geometry_msgs</depend>


  <test_depend>ament_copyright</test_depend>
  <test_depend>ament_flake8</test_depend>
  <test_depend>ament_pep257</test_depend>
  <test_depend>python3-pytest</test_depend>

  <export>
    <build_type>ament_python</build_type>
  </export>
</package>
```

Por fim, compile o pacote e rode o nó:
```bash
cd ~/master_ros2_ws
colcon build --packages-select controle_simulacao
source install/setup.bash
ros2 run controle_simulacao circulo
```
---

## 9. Desafio Técnico
Após rodar o script e observar o robô no Gazebo e no RViz2, responda:
1.  **Análise de Desvio:** No RViz2, o rastro da odometria (`Odometry`) fecha um círculo perfeito após 5 voltas?
2.  **Referencial:** Se alterarmos o **Fixed Frame** no RViz2 de `odom` para `base_link`, o que acontece com a visualização do robô e do laser? Por que isso ocorre?