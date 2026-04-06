# Roteiro Prático: Simulação e Inspeção de Dados no ROS 2 Jazzy

## 1. Objetivos
* Configurar o ambiente para o **TurtleBot3 Waffle** no Ubuntu 24.04.
* Lançar o mundo de simulação no Gazebo e inspecionar a física.
* Utilizar ferramentas de diagnóstico (`rqt_graph` e `ros2 topic`).
* Configurar o **RViz2** manualmente para visualização de sensores (LiDAR e Odometria).

---

## 2. Configuração do Ambiente
Antes de iniciar, precisamos garantir que as variáveis de ambiente e os pacotes necessários estejam instalados. Execute no terminal:

```bash
# Instalação das dependências do TurtleBot3 para Jazzy
sudo apt update
sudo apt install ros-jazzy-turtlebot3-simulations ros-jazzy-turtlebot3-description

# Definição do modelo do robô (adicione ao seu .bashrc para persistência)
export TURTLEBOT3_MODEL=waffle
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:/opt/ros/jazzy/share/turtlebot3_gazebo/models
```

---

## 3. Lançando a Simulação
Este comando inicializa o motor de física Gazebo, carrega o mundo de obstáculos e o nó `robot_state_publisher` que gerencia a árvore de transformadas (TF).

```bash
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```
> **Dica:** O Gazebo pode demorar um pouco no primeiro carregamento para baixar os modelos. Aguarde até ver o robô posicionado no centro do mapa.

---

## 4. Inspeção do Grafo e Fluxo de Dados
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

## 5. Visualização Avançada no RViz2
O RViz2 é essencial para depurar o que o robô "vê". Ele inicia vazio, e você deve configurá-lo manualmente:

1.  No terminal, digite: `rviz2`
2.  No painel **Global Options**, altere o **Fixed Frame** para `odom`.
3.  Clique em **Add** e adicione os seguintes displays:
    * **RobotModel**: Renderiza o Waffle em 3D.
    * **TF**: Mostra os eixos coordenados. Identifique o `base_link` e o `odom`.
    * **LaserScan**: Defina o tópico como `/scan`. (Sugestão: mude o *Style* para `Points` e *Size* para `0.03`).
    * **Odometry**: Defina o tópico como `/odom`. Isso mostrará o rastro do robô.



---

## 6. Implementação: Controle de Malha Aberta (Python)
Crie um diretório chamado `scripts` e salve o arquivo abaixo como `circulo.py`. O objetivo é aplicar a **Cinemática Direta** para realizar uma trajetória circular.

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

---

## 7. Desafio Técnico
Após rodar o script e observar o robô no Gazebo e no RViz2, responda:
1.  **Análise de Desvio:** No RViz2, o rastro da odometria (`Odometry`) fecha um círculo perfeito após 5 voltas?
2.  **Referencial:** Se alterarmos o **Fixed Frame** no RViz2 de `odom` para `base_link`, o que acontece com a visualização do robô e do laser? Por que isso ocorre?