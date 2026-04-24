# Aula 6: Navegação Programática e Patrulha de Waypoints (Nav2)

## 1. Objetivos
* Transitar da navegação manual via interface (RViz2) para a navegação programática.
* Compreender a estrutura da mensagem `geometry_msgs/msg/PoseStamped`.
* Desenvolver um nó em Python que publica uma sequência de coordenadas no tópico `/goal_pose`, atuando como um despachante de missões.
* Observar na prática os efeitos das Zonas de Inflação (Costmaps) e a importância de evitar concorrência de comandos no planejamento local.

---

## 2. Fundamentação Teórica Breve

Na Aula 5, utilizamos a interface gráfica do RViz2 para mandar o robô andar. Nos bastidores, ao clicar no mapa, o sistema empacota os dados de $(x, y)$ em uma mensagem do tipo `PoseStamped` e publica no tópico `/goal_pose`. A pilha do Nav2 escuta esse tópico e inicia o planejamento.

Nesta aula, o nosso script Python assumirá o papel do mouse. A grande diferença da navegação autônoma em relação à cinemática da Aula 4 é que não enviaremos mais velocidades diretas aos motores (`/cmd_vel`). Enviaremos **intenções geográficas** no referencial `map`. O Nav2 se encarregará de transformar essas intenções nas velocidades de roda corretas, desviando dos obstáculos.

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
2.  **Terminal 2 (Ponte GZ-ROS - caso necessário):**
    ```bash
    ros2 run ros_gz_bridge parameter_bridge /cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist
    ```
3.  **Terminal 3 (Navegação):** Utilize o mapa gerado e salvo na Aula 5 (`mapa_lab.yaml`).
    ```bash
    ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True map:=$HOME/mapa_lab.yaml
    ```
4.  **Estimativa de Pose (AMCL):** No RViz2, utilize o botão **2D Pose Estimate** para localizar o robô no mapa inicial. Se o robô não souber onde está no referencial `map`, ele rejeitará qualquer coordenada de destino.

---

## 4. Obtendo as Coordenadas de Patrulha (Método Visual)

Para que o robô patrulhe, precisamos fornecer pontos (x, y) que existam no espaço livre do seu mapa. A forma mais rápida e prática de descobrir essas coordenadas é utilizando a própria grade (grid) do RViz2 para fazer uma estimativa visual.

1. Observe o chão quadriculado (Grid) no RViz2. Por padrão, cada quadrado cinza tem a medida exata de **1 metro por 1 metro**.
2. O ponto de origem **x: 0.0, y: 0.0** é o local exato onde o robô "nasceu" no mapa inicial.
3. Para escolher um ponto de patrulha, basta contar os quadrados a partir do centro do robô:
   * **Eixo X (Seta Vermelha):** Quadrados para a frente são positivos.
   * **Eixo Y (Seta Verde):** Quadrados para a esquerda são positivos.
4. Anotaremos as estimativas visuais para utilizar no nosso código.

---

## 5. Implementação Prática: A Primeira Versão (Ingênua)

Nossa primeira tentativa de criar um patrulheiro utilizará uma lógica simples baseada em um Temporizador (Timer) e nas coordenadas estimadas visualmente.

No seu pacote `controle_simulacao`, crie o arquivo `patrulheiro.py` e insira o código abaixo. Preste atenção nas coordenadas definidas na lista `self.waypoints`.

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped
import math

class PatrulheiroNav2(Node):
    def __init__(self):
        super().__init__('patrulheiro_node')
        
        self.publisher_ = self.create_publisher(PoseStamped, '/goal_pose', 10)
        self.subscription = self.create_subscription(PoseWithCovarianceStamped, '/amcl_pose', self.pose_callback, 10)

        # Pontos da primeira tentativa (Coordenadas "Ingênuas")
        self.waypoints = [
            (2.0, 0.0, 0.0),    
            (2.0, 2.0, 1.57),   
            (0.0, 2.0, 3.14),   
            (0.0, 0.0, -1.57)   
        ]
        
        self.indice_atual = 0
        self.objetivo_ativo = False
        self.tolerancia_chegada = 0.35  

        # Timer: Tenta forçar o robô a lembrar do destino a cada 2 segundos
        self.timer = self.create_timer(2.0, self.timer_callback)
        
        self.get_logger().info('Script iniciado! Dê o "2D Pose Estimate" no RViz2 para dar o gatilho...')

    def euler_to_quaternion(self, yaw):
        qx = 0.0
        qy = 0.0
        qz = math.sin(yaw / 2.0)
        qw = math.cos(yaw / 2.0)
        return qx, qy, qz, qw

    def enviar_objetivo(self):
        if self.indice_atual < len(self.waypoints):
            x, y, yaw = self.waypoints[self.indice_atual]
            
            msg = PoseStamped()
            msg.header.frame_id = 'map'
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.pose.position.x = x
            msg.pose.position.y = y
            msg.pose.position.z = 0.0

            qx, qy, qz, qw = self.euler_to_quaternion(yaw)
            msg.pose.orientation.x = qx
            msg.pose.orientation.y = qy
            msg.pose.orientation.z = qz
            msg.pose.orientation.w = qw

            self.publisher_.publish(msg)
            self.get_logger().info(f'Patrulhando Waypoint {self.indice_atual + 1}: x={x:.2f}, y={y:.2f}')
            self.objetivo_ativo = True
        else:
            self.get_logger().info('Circuito concluído! Reiniciando...')
            self.indice_atual = 0 

    def timer_callback(self):
        if self.objetivo_ativo:
            self.enviar_objetivo()

    def pose_callback(self, msg):
        if not self.objetivo_ativo:
            self.enviar_objetivo()
            return

        atual_x = msg.pose.pose.position.x
        atual_y = msg.pose.pose.position.y
        alvo_x, alvo_y, _ = self.waypoints[self.indice_atual]

        distancia = math.sqrt((alvo_x - atual_x)**2 + (alvo_y - atual_y)**2)

        if distancia < self.tolerancia_chegada:
            self.get_logger().info(f'>>> Destino alcançado!')
            self.indice_atual += 1
            self.objetivo_ativo = False 

def main(args=None):
    rclpy.init(args=args)
    node = PatrulheiroNav2()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

Compile o pacote (`colcon build`) e execute o script:
```bash
ros2 run controle_simulacao patrulheiro
```
**Atenção:** Dê o comando de *2D Pose Estimate* no RViz2 para iniciar. 

**O que aconteceu?**
Você notará que o robô provavelmente percorrerá apenas a primeira reta e depois **travará completamente**, recusando-se a ir para a coordenada `(2.0, 2.0)`, mesmo com o script rodando.

---

## 6. Estudo de Caso de Engenharia: Por que o Robô Falhou?

O robô não travou por causa de um "bug" de compilação, mas sim por uma violação conceitual das regras de navegação. Nosso script inicial cometeu dois erros clássicos de controle autônomo:



### Falha 1: Ignorando o Mapa de Custo (Costmap Inflation)
Observe o mapa no seu RViz2. Ao redor dos pilares (obstáculos brancos), o Nav2 desenha "auréolas" coloridas:
* **Ciano/Azul Escuro:** Custo Letal (É o espaço físico ocupado pelo objeto e pela largura do chassi do robô).
* **Roxo/Vermelho:** Zona de Inflação (A margem de segurança extra).

**A Regra de Ouro do Nav2:** O planejador global se recusa estritamente a traçar uma rota cujo destino final caia dentro das zonas de inflação (Ciano/Roxo). Ao chutarmos a coordenada `(2.0, 2.0)`, nós acidentalmente mandamos o robô estacionar "dentro" do campo de força do pilar. Como a matemática prova que isso resultaria em colisão, o Nav2 simplesmente aborta a missão por segurança.

### Falha 2: Concorrência e Sobrecarga de Comandos ("Spamming")
Na nossa lógica, criamos um `timer_callback` que republicava a mesma coordenada a cada 2 segundos. No ROS 2, toda vez que o tópico `/goal_pose` recebe uma mensagem, o Nav2 assume que é uma **nova ordem**, cancelando imediatamente os cálculos atuais da trajetória para refazer a matemática do zero. 
Ao "bombardear" o tópico com mensagens repetidas, induzimos um "Stuttering" (gagueira) no planejador local (DWA), fazendo o robô ficar congelado pensando em vez de andar.

---

## 7. Refatoração: O Script Robusto

Para construir um sistema confiável, precisamos remover o temporizador (enviando a ordem apenas uma vez) e escolher rotas que passem estritamente pelo "corredor branco" seguro (espaço livre). 

Edite o seu `patrulheiro.py` substituindo-o por esta versão otimizada:

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped
import math

class PatrulheiroNav2(Node):
    def __init__(self):
        super().__init__('patrulheiro_node')
        
        self.publisher_ = self.create_publisher(PoseStamped, '/goal_pose', 10)
        self.subscription = self.create_subscription(PoseWithCovarianceStamped, '/amcl_pose', self.pose_callback, 10)

        # WAYPOINTS SEGUROS: Coordenadas precisas que caem nas áreas brancas do Costmap
        self.waypoints = [
            (1.0, 0.0, 0.0),    # Corredor seguro à frente
            (1.0, 1.0, 1.57),   # Vira e sobe para o próximo corredor
            (0.0, 1.0, 3.14),   # Move para a esquerda em área limpa
            (0.0, 0.0, -1.57)   # Retorna à origem
        ]
        
        self.indice_atual = 0
        self.objetivo_ativo = False
        self.tolerancia_chegada = 0.35  

        self.get_logger().info('Script iniciado! Dê o "2D Pose Estimate" no RViz2 para dar o gatilho...')

    def euler_to_quaternion(self, yaw):
        qx = 0.0
        qy = 0.0
        qz = math.sin(yaw / 2.0)
        qw = math.cos(yaw / 2.0)
        return qx, qy, qz, qw

    def enviar_objetivo(self):
        if self.indice_atual < len(self.waypoints):
            x, y, yaw = self.waypoints[self.indice_atual]
            
            msg = PoseStamped()
            msg.header.frame_id = 'map'
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.pose.position.x = x
            msg.pose.position.y = y
            msg.pose.position.z = 0.0

            qx, qy, qz, qw = self.euler_to_quaternion(yaw)
            msg.pose.orientation.x = qx
            msg.pose.orientation.y = qy
            msg.pose.orientation.z = qz
            msg.pose.orientation.w = qw

            self.publisher_.publish(msg)
            self.get_logger().info(f'Enviando objetivo único para Waypoint {self.indice_atual + 1}: x={x:.2f}, y={y:.2f}')
            
            # Marca que a ordem foi dada, impedindo que seja enviada novamente
            self.objetivo_ativo = True
        else:
            self.get_logger().info('Circuito concluído! Reiniciando a patrulha...')
            self.indice_atual = 0 
            self.objetivo_ativo = False

    def pose_callback(self, msg):
        # Transição de Estado: Só envia se estiver ocioso
        if not self.objetivo_ativo:
            self.enviar_objetivo()
            return

        atual_x = msg.pose.pose.position.x
        atual_y = msg.pose.pose.position.y
        alvo_x, alvo_y, _ = self.waypoints[self.indice_atual]

        distancia = math.sqrt((alvo_x - atual_x)**2 + (alvo_y - atual_y)**2)

        if distancia < self.tolerancia_chegada:
            self.get_logger().info(f'>>> Sucesso! Destino {self.indice_atual + 1} alcançado (Erro: {distancia:.2f}m)')
            self.indice_atual += 1
            
            # Libera a trava lógica para que o próximo ponto seja enviado
            self.objetivo_ativo = False 

def main(args=None):
    rclpy.init(args=args)
    node = PatrulheiroNav2()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Operação interrompida.')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

Após rodar o comando `colcon build` novamente, execute o script e ative o *2D Pose Estimate*. O robô agora navegará com fluidez pelas zonas livres, demonstrando a robustez de um controle que respeita o mapa de custo e não sobrecarrega a rede.

---

## 8. Desafio Analítico para o Relatório

1.  **Quaternions na Prática:** Analise a função `euler_to_quaternion` do código. Se o objetivo fosse posicionar o robô virado 90 graus positivos em relação ao referencial `map`, quais seriam os valores finais exatos das variáveis `qz` e `qw`? Demonstre o cálculo.
2.  **Agressividade do Planejamento:** Na nossa primeira versão com falha, o Nav2 abortou o trajeto inteiro porque a última coordenada era inválida. Se em um projeto de indústria você precisasse forçar o robô a ir o *mais perto possível* daquela coordenada `(2.0, 2.0)` proibida, como você configuraria os parâmetros do Nav2 para aceitar uma aproximação parcial em vez de desistir da missão?
3.  **Comparação de Malhas:** Qual é a diferença fundamental entre a leitura de *feedback* feita na Aula 5 (onde assinamos `/scan`) e a feita hoje (onde assinamos `/amcl_pose`) em termos de referencial espacial (Local vs. Global)?