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
## 4. Instalação do ambiente de simulação e do modelo do robô Turtlebot 3

Vamos executar um script que está no repositório da disciplina, que você acabou de baixar no item 3:
```bash
cd ~/cont-int-2026-1/modulo_simulacao_1/scripts
chmod +x install_tb3_jazzy.sh
./install_tb3_jazzy.sh
```
Com esse script você garante toda a configuração necessária para ter seu ambiente de simulação com o Turtlebot 3.


---

## 5. Lançando a Simulação
Este comando inicializa o motor de física Gazebo, carrega o mundo de obstáculos e o nó `robot_state_publisher` que gerencia a árvore de transformadas (TF).

```bash
export TURTLEBOT3_MODEL=waffle
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```
> **Dica:** O Gazebo pode demorar um pouco no primeiro carregamento para baixar os modelos. Aguarde até ver o robô posicionado no centro do mapa.

---

## 6. Habilitando a Comunicação (A PONTE)
No ROS 2 Jazzy, o Gazebo Sim fala uma "língua" diferente do ROS. Precisamos de uma ponte (bridge) para traduzir as mensagens de velocidade. **Abra um novo terminal** e execute:

```bash
ros2 run ros_gz_bridge parameter_bridge /cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist
```
*Mantenha este terminal aberto durante toda a simulação.*

---

## 7. Controle Manual do Robô
Agora vamos interagir com o robô. Abra um **novo terminal** e execute o seguinte comando:

```bash
export TURTLEBOT3_MODEL=waffle
ros2 run turtlebot3_teleop teleop_keyboard
```
Clique na janela  em que você entrou com os comandos acima e utilize as teclas (w, a, s, d) e para controlar o robô.
Aqui está a tradução dos comandos de teleoperação para o seu material:

**Movimentação:**
```text
        w
   a    s    d
        x
```

* **w / x :** aumentar / diminuir velocidade linear (Burger: ~ 0.22, Waffle e Waffle Pi: ~ 0.26)
* **a / d :** aumentar / diminuir velocidade angular (Burger: ~ 2.84, Waffle e Waffle Pi: ~ 1.82)
* **barra de espaço, s :** parada forçada (parar imediatamente)
---

## 8. Inspeção do Grafo e Fluxo de Dados
Abra um **novo terminal** e utilize as ferramentas de introspecção do ROS 2:

1.  **Grafo de Nós:** `rqt_graph`(Selecione a opção *Nodes/Topics(all)* e clique no botão de atualizar)
    * Observe como o nó `/ros_gz_bridge` se comunica com os demais.
2.  **Lista de Tópicos:** `ros2 topic list`
    * Verifique a existência dos tópicos `/cmd_vel`, `/odom`, `/scan` e `/tf`.
3.  **Frequência de Atualização:** Escolha o tópico do laser e verifique a taxa de publicação:
    ```bash
    ros2 topic hz /scan
    ```

---

## 9. Visualização Avançada no RViz2
O RViz2 é essencial para depurar o que o robô "vê". Ele inicia pode iniciar vazio, e você deve configurá-lo:

Use o seguinte lançador:
```bash
ros2 launch turtlebot3_bringup rviz2.launch.py
```

1.  No painel **Global Options**, altere o **Fixed Frame** para `odom`.
2.  Antes de cada item abaixo clique em **Add**na aba **By display type**$\rightarrow$**rviz_default_plugins** adicione os seguintes displays:
    * **RobotModel**: Renderiza o Waffle em 3D.
    * **TF**: Mostra os eixos coordenados. Na opção **TF**$\rightarrow$**Frames** habilite os frames `base_link` e `odom`.
3.  Antes de cada item abaixo clique em **Add**na aba **By topic**:
    * **LaserScan**: selecione o tópico  `/scan`$\rightarrow$`LaserScan`. (Sugestão: mude o *Style* para `Points` e *Size* para `0.03` pixels).
    * **Odometry**: selecione o tópico `/odom`$\rightarrow$`Odometry`. Isso mostrará o rastro do robô.
    * **Camera**: selecione o tópico `/camera/image_raw`$\rightarrow$`Camera`.

Faça também os seguintes ajustes em **Odometry**:
* Ajuste Dimensional das Setas
    * **Shaft Length (Comprimento do corpo):** Mude para **0.02**.
    * **Shaft Radius (Raio do corpo):** Mude para **0.001** (ou menor).
    * **Head Length (Comprimento da ponta):** Mude para **0.002**.
    * **Head Radius (Raio da ponta):** Mude para **0.002**.

Isso fará com que cada registro de odometria seja apenas uma pequena marcação, permitindo ver a trajetória sem cobrir o robô.

* Configuração do Histórico (Rastro)
Para que o rastro não desapareça e eles consigam ver o círculo completo (e as voltas subsequentes), ajuste:
    * **Keep (ou Buffer):** Aumente para **500**.
    * **Color:** Escolha uma cor contrastante (ex: Verde Limão ou Ciano) para destacar do fundo cinza.

---

## 10. Implementação: Controle de Malha Aberta (Python)
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

Interrompa a execução do terminal(`CTRL+C`) em que você usou o `teleop_keyboard` para o controle manual. 


Por fim, compile o pacote e rode o nó:
```bash
cd ~/master_ros2_ws
colcon build --packages-select controle_simulacao
source install/setup.bash
ros2 run controle_simulacao circulo
```
