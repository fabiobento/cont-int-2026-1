# Aula 5: Mapeamento Autônomo (SLAM) e Navegação no ROS 2 Jazzy

##  1. Objetivos
* Programar um nó de controle reativo em Python para exploração autônoma (Malha Fechada).
* Operar o algoritmo Cartographer (SLAM) para construir um mapa digital do ambiente sem intervenção manual.
* Salvar o mapa de grade de ocupação no sistema local.
* Executar a pilha do Nav2 e a Estimativa de Pose (AMCL) para planejar trajetórias e desviar de obstáculos de forma autônoma.

---

##  2. Etapa A: O Desafio de Programação (Python)

Em vez de usar o teclado para mover o robô durante o mapeamento, criaremos um script que assina o tópico `/scan` (LiDAR) e publica comandos em `/cmd_vel` (Motores).

1. No seu pacote `controle_simulacao`, crie um novo arquivo chamado `explorador.py`.
2. Utilize o código base abaixo. O algoritmo segue uma lógica simples: se o caminho à frente estiver livre, avance; se detectar um obstáculo a menos de 0.7 metros, gire para desviar.

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import math

class ExploradorReativo(Node):
    def __init__(self):
        super().__init__('explorador_node')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.subscription = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        
        # Aumentamos um pouco a margem para evitar que o chassi raspe na parede
        self.distancia_segura = 0.8  

    def scan_callback(self, msg):
        twist = Twist()
        
        # 1. Criação do Cone de Visão (60 graus frontais)
        # O LiDAR retorna 360 leituras (índices 0 a 359).
        # Pegamos 30 graus para a esquerda (0 a 29) e 30 graus para a direita (330 a 359)
        visao_esquerda = msg.ranges[0:30]
        visao_direita = msg.ranges[330:360]
        cone_frontal = visao_esquerda + visao_direita
        
        # 2. Limpeza de Dados
        # Remove leituras 'inf' ou 'NaN' (típicas do simulador quando o laser não bate em nada)
        cone_limpo = [dist for dist in cone_frontal if not math.isinf(dist) and not math.isnan(dist)]
        
        # 3. Identifica a menor distância dentro do cone
        if len(cone_limpo) > 0:
            menor_distancia = min(cone_limpo)
        else:
            menor_distancia = 3.5 # Se tudo for infinito, assume caminho livre
        
        # 4. Lógica de Controle Reativo
        if menor_distancia < self.distancia_segura:
            # Obstáculo no cone! Para de andar para frente e gira mais rápido.
            twist.linear.x = 0.0
            twist.angular.z = 0.8  # Aumentado de 0.5 para 0.8 rad/s para manobrar ágil
            self.get_logger().info(f'Obstáculo a {menor_distancia:.2f}m no cone! Girando...')
        else:
            # Caminho livre! Pode acelerar.
            twist.linear.x = 0.22  # Aumentado de 0.15 para 0.22 m/s (mais rápido)
            twist.angular.z = 0.0

        self.publisher_.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = ExploradorReativo()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.publisher_.publish(Twist()) # Parada de segurança ao dar Ctrl+C
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```
3. Lembre-se de adicionar `'explorador = controle_simulacao.explorador:main'` no `setup.py` e compilar o pacote com o `colcon build`.

---

##  3. Etapa B: Mapeamento Autônomo (SLAM)

Agora colocaremos o robô para mapear o ambiente sozinho, executando os três pilares simultaneamente.

1. **Inicie o Simulador:**
   ```bash
   export TURTLEBOT3_MODEL=waffle
   ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
   ```
2. **Inicie o Nó de SLAM (Cartographer):**
   Abra um novo terminal e execute:
   ```bash
   export TURTLEBOT3_MODEL=waffle
   ros2 launch turtlebot3_cartographer cartographer.launch.py use_sim_time:=True
   ```
3. Habilitando a Comunicação (A PONTE)
    
    No ROS 2 Jazzy, o Gazebo Sim fala uma "língua" diferente do ROS. Precisamos de uma ponte (bridge) para traduzir as mensagens de velocidade. **Abra um novo terminal** e execute:

    ```bash
    ros2 run ros_gz_bridge parameter_bridge /cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist
    ```
*Mantenha este terminal aberto durante toda a simulação.*

4. **Inicie o Explorador Autônomo:**
   Em um terceiro terminal, rode o nó que você acabou de programar:
   ```bash
   ros2 run controle_simulacao explorador
   ```
   *Observe no RViz2 o robô navegando sozinho e construindo o mapa dinamicamente.*
5. **Salve o Mapa:**
   Após o ambiente estar completamente mapeado, abra um quarto terminal e salve os dados:
   ```bash
   ros2 run nav2_map_server map_saver_cli -f ~/mapa_lab
   ```
   *(Isso gerará os arquivos `mapa_lab.pgm` e `mapa_lab.yaml` na sua pasta).*

---

##  4. Etapa C: Navegação e AMCL (Nav2)

Encerre (Ctrl+C) o nó de SLAM e o seu nó `explorador`. Mantenha apenas o simulador Gazebo aberto.

1. **Inicie a Navegação com o mapa salvo:**
   ```bash
   export TURTLEBOT3_MODEL=waffle
   ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True map:=$HOME/mapa_lab.yaml
   ```
2. **Estimativa de Pose Inicial (AMCL):** O algoritmo AMCL alinha a posição real do robô com o mapa estático.
   * Clique em **2D Pose Estimate** no menu do RViz2.
   * Clique no local do mapa onde o robô se encontra no Gazebo e arraste a seta indicando para onde a frente dele aponta.
3. **Envie um Destino:**
   * Clique em **Nav2 Goal** no RViz2, selecione um destino no mapa e indique a orientação final desejada. 
   * O Nav2 calculará a rota desviando de paredes e obstáculos autônomamente.

---

##  5. Desafio Analítico para o Relatório

Com base no que foi visto nas últimas aulas e nesta prática, responda no seu relatório:

1. **Observação de Frames:** Durante a navegação (Etapa C), o *Fixed Frame* no RViz2 geralmente está configurado para `map`. Como o referencial `map` se diferencia do referencial `odom` (visto na Aula 4) em termos de estabilidade a longo prazo? O que o algoritmo AMCL faz com essa relação?
2. **Obstáculos Dinâmicos:** Observe o rastro colorido (Global Path e Local Path) que aparece no mapa durante o movimento. Explique como a pilha do Nav2 utiliza o mapa salvo (estático) e os dados em tempo real do LiDAR (dinâmicos) simultaneamente para evitar colisões com objetos que não existiam durante a Etapa B.
3. **O Problema do Beco sem Saída:** Imagine que o robô seja colocado dentro de um corredor em formato de "U". Descreva como o seu script Python `explorador.py` se comportaria nessa situação em comparação à inteligência da pilha do Nav2. Use os conceitos de "controle reativo" (sem memória) e "planejamento global" para justificar sua resposta.

---