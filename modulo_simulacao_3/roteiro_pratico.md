# Aula 6: Navegação Programática e Patrulha de Waypoints (Nav2)

## 1. Objetivos
* Evoluir da navegação manual via interface (RViz2) para a navegação programática.
* Compreender a estrutura da mensagem `geometry_msgs/msg/PoseStamped`.
* Desenvolver um nó em Python que publica uma sequência de coordenadas no tópico `/goal_pose`, atuando como um despachante de missões.
* Aplicar uma malha de controle baseada em distância euclidiana monitorando o tópico `/amcl_pose` para determinar a chegada ao destino.

---

## 2. Fundamentação Teórica Breve

Na Aula 5, utilizamos o botão **Nav2 Goal** no RViz2. Nos bastidores, esse botão captura a coordenada $(x, y)$ onde o mouse clicou e o ângulo $\theta$ gerado ao arrastar a seta, empacota esses dados em uma mensagem do tipo `PoseStamped` e publica no tópico `/goal_pose`. A pilha do Nav2 escuta esse tópico e inicia o planejamento.

Nesta aula, o script Python assumirá o papel do mouse. A grande diferença da navegação autônoma em relação à cinemática da Aula 4 é que não enviaremos mais velocidades aos motores (`/cmd_vel`). Enviaremos **intenções geográficas** no referencial `map`. O Nav2 se encarregará de transformar essas intenções nas velocidades de roda corretas, desviando dos obstáculos.

---

## 3. Isolamento e Preparação do Ambiente

Para garantir que os robôs do laboratório operem sem interferências mútuas durante o teste das patrulhas, ative o isolamento de rede em cada terminal que for abrir:
```bash
export ROS_DOMAIN_ID=XX  # Substitua XX pelo número da sua bancada
export TURTLEBOT3_MODEL=waffle
```

Precisaremos do ecossistema completo rodando antes de iniciar nosso código:

1.  **Terminal 1 (Gazebo):**
    ```bash
    ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
    ```
2.  **Terminal 2 (Ponte GZ-ROS - caso necessário no Jazzy):**
    ```bash
    ros2 run ros_gz_bridge parameter_bridge /cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist
    ```
3.  **Terminal 3 (Navegação):** Utilize o mapa gerado e salvo na Aula 5 (`mapa_lab.yaml`).
    ```bash
    ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True map:=$HOME/mapa_lab.yaml
    ```
4.  **Estimativa de Pose (AMCL):** No RViz2, utilize o botão **2D Pose Estimate** para localizar o robô no mapa inicial. Se o robô não souber onde está no referencial `map`, ele rejeitará qualquer coordenada de destino.

---

## 4. Obtendo as Coordenadas de Patrulha (Waypoints)

Para que o robô patrulhe, precisamos fornecer pontos $(x, y)$ que existam no espaço livre do seu mapa.
Para descobrir essas coordenadas sem tentar "adivinhar":
1. Abra um novo terminal e monitore o tópico de destino:
   ```bash
   ros2 topic echo /goal_pose
   ```
2. No RViz2, clique no botão **Nav2 Goal** e marque um ponto no mapa.
3. O terminal imprimirá a mensagem gerada. Anote os valores de `x` e `y` do bloco `position`. Escolha de 3 a 4 pontos diferentes pelo mapa para compor a sua rota de patrulha.

---

## 5. Implementação: O Nó Patrulheiro

No seu pacote `controle_simulacao`, crie um novo arquivo chamado `patrulheiro.py`.

A lógica de programação utilizará um fechamento de malha simples: publicamos o objetivo em `/goal_pose` e ficamos ouvindo o tópico `/amcl_pose` (que nos diz a localização estimada atual do robô). Calculamos a distância entre onde o robô está e o nosso objetivo. Quando essa distância for menor que um limite de tolerância (ex: $0.3$ metros), avançamos para a próxima coordenada da lista.

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped
import math

class PatrulheiroNav2(Node):
    def __init__(self):
        super().__init__('patrulheiro_node')
        
        # Publisher para enviar o destino ao Nav2
        self.publisher_ = self.create_publisher(PoseStamped, '/goal_pose', 10)
        
        # Subscriber para saber a pose atual estimada no mapa
        self.subscription = self.create_subscription(
            PoseWithCovarianceStamped, 
            '/amcl_pose', 
            self.pose_callback, 
            10
        )

        # INSIRA AQUI OS SEUS PONTOS (x, y, yaw em radianos)
        # Exemplo de rota quadrada no centro do mapa
        self.waypoints = [
            (1.5, 0.0, 0.0),
            (1.5, 1.5, 1.57),
            (0.0, 1.5, 3.14),
            (0.0, 0.0, -1.57)
        ]
        
        self.indice_atual = 0
        self.objetivo_ativo = False
        self.tolerancia_chegada = 0.35  # Distância de aceite em metros

        # Timer para reenviar a meta, garantindo que o Nav2 não a perca
        self.timer = self.create_timer(2.0, self.timer_callback)

    def euler_to_quaternion(self, yaw):
        """
        Converte o ângulo de orientação (yaw) de radianos para Quaternions.
        O Nav2 exige que a orientação seja enviada neste formato.
        """
        qx = 0.0
        qy = 0.0
        qz = math.sin(yaw / 2.0)
        qw = math.cos(yaw / 2.0)
        return qx, qy, qz, qw

    def enviar_objetivo(self):
        if self.indice_atual < len(self.waypoints):
            x, y, yaw = self.waypoints[self.indice_atual]
            
            # Montagem da mensagem PoseStamped
            msg = PoseStamped()
            msg.header.frame_id = 'map'
            msg.header.stamp = self.get_clock().now().to_msg()

            msg.pose.position.x = x
            msg.pose.position.y = y
            msg.pose.position.z = 0.0

            # Aplicação da conversão matemática
            qx, qy, qz, qw = self.euler_to_quaternion(yaw)
            msg.pose.orientation.x = qx
            msg.pose.orientation.y = qy
            msg.pose.orientation.z = qz
            msg.pose.orientation.w = qw

            self.publisher_.publish(msg)
            self.get_logger().info(f'Patrulhando Waypoint {self.indice_atual + 1}: alvo em x={x:.2f}, y={y:.2f}')
            self.objetivo_ativo = True
        else:
            self.get_logger().info('Circuito concluído! Reiniciando a patrulha...')
            self.indice_atual = 0 

    def timer_callback(self):
        # Publica periodicamente a intenção caso a primeira mensagem tenha sido descartada pelo Nav2
        if self.objetivo_ativo:
            self.enviar_objetivo()

    def pose_callback(self, msg):
        if not self.objetivo_ativo:
            self.enviar_objetivo()
            return

        # Coordenadas reais atuais do robô (vindas do AMCL)
        atual_x = msg.pose.pose.position.x
        atual_y = msg.pose.pose.position.y

        # Coordenadas do objetivo atual
        alvo_x, alvo_y, _ = self.waypoints[self.indice_atual]

        # Cálculo da distância Euclidiana d = sqrt((x2 - x1)² + (y2 - y1)²)
        distancia = math.sqrt((alvo_x - atual_x)**2 + (alvo_y - atual_y)**2)

        # Lógica de transição de estado
        if distancia < self.tolerancia_chegada:
            self.get_logger().info(f'>>> Chegamos no destino {self.indice_atual + 1} com erro residual de {distancia:.2f}m')
            self.indice_atual += 1
            self.objetivo_ativo = False # Prepara para o próximo envio

def main(args=None):
    rclpy.init(args=args)
    node = PatrulheiroNav2()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Patrulha interrompida pelo usuário.')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Configuração do Pacote
Não se esqueça de adicionar o novo nó no arquivo `setup.py` dentro do bloco `console_scripts`:
```python
'patrulheiro = controle_simulacao.patrulheiro:main',
```
Em seguida, compile o pacote na raiz do seu workspace (`colcon build --packages-select controle_simulacao`) e carregue as variáveis com `source install/setup.bash`.

---

## 6. Execução e Inspeção
Com o simulador, a ponte e a navegação rodando, execute o seu patrulheiro:
```bash
ros2 run controle_simulacao patrulheiro
```
Acompanhe o comportamento no RViz2. Você observará o caminho global sendo traçado dinamicamente de um ponto a outro assim que a distância euclidiana estipulada for atingida. 

Para testar a robustez do planejador local, adicione um objeto novo (como um cubo) no Gazebo exatamente na rota de patrulha do robô e observe a alteração da trajetória gerada em tempo real para o alcance do Waypoint.

---

## 7. Desafio Analítico para o Relatório

1.  **Quaternions na Prática:** Analise a função `euler_to_quaternion` do código. Se o objetivo fosse posicionar o robô virado $90^\circ$ positivos (ou seja, $\pi/2$ radianos) em relação ao referencial `map`, quais seriam os valores finais exatos das variáveis `qz` e `qw`? Demonstre o cálculo.
2.  **O Papel da Tolerância:** A variável `tolerancia_chegada` foi definida como $0.35$ metros. O que ocorreria dinamicamente com o robô (e com o loop do script) se esse valor fosse reduzido drasticamente para $0.01$ metros, considerando as restrições físicas do TurtleBot3 e a tolerância padrão de chegada do algoritmo Nav2?
3.  **Comparação de Malhas:** Qual é a diferença fundamental entre a leitura de *feedback* feita na Aula 5 (onde assinamos `/scan`) e a feita hoje (onde assinamos `/amcl_pose`) em termos de referencial espacial (Local vs. Global)?