# Aula 6: Navegação Programática, Costmaps e Sintonia Fina (Tuning)

## 1. Objetivos
* Transitar da navegação manual via interface (RViz2) para a navegação programática usando Python.
* Compreender a estrutura da mensagem `geometry_msgs/msg/PoseStamped`.
* Aprofundar a teoria de **Mapas de Custo (Costmaps)** e suas camadas de inflação.
* Utilizar a ferramenta **RQT** para realizar a sintonia fina (*tuning*) de parâmetros dinâmicos em tempo de execução para resolver impasses de navegação.

---

## 2. Fundamentação Teórica Breve

Na Aula 5, utilizamos a interface gráfica do RViz2 para mandar o robô andar. Ao clicar no mapa, o sistema empacota os dados de $(x, y)$ em uma mensagem do tipo `PoseStamped` e publica no tópico `/goal_pose`. 

Nesta aula, nosso script Python assumirá o papel do mouse, enviando **intenções geográficas** no referencial `map`. O Nav2 se encarregará de transformar essas intenções nas velocidades de roda corretas, desviando dos obstáculos. No entanto, veremos que o robô não obedece a ordens cegamente: ele avalia rigorosamente a viabilidade matemática de cada coordenada antes de se mover.

---

## 3. Isolamento e Preparação do Ambiente

Ative o isolamento de rede em cada terminal que for abrir:
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
3.  **Terminal 3 (Navegação):** Utilize o mapa gerado na Aula 5 (`mapa_lab.yaml`).
    ```bash
    ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True map:=$HOME/mapa_lab.yaml
    ```
4.  **Estimativa de Pose (AMCL):** No RViz2, utilize o botão **2D Pose Estimate** para localizar o robô no mapa inicial. Se o robô não souber onde está no referencial `map`, ele rejeitará qualquer coordenada.

---

## 4. Implementação Prática: A Primeira Versão (Ingênua)

Nossa primeira tentativa de criar um patrulheiro utilizará uma lógica simples baseada em um Temporizador (Timer). Vamos tentar forçar o robô a passar bem perto de um dos pilares do labirinto (coordenada `2.0, 2.0`).

No seu pacote `controle_simulacao`, crie o arquivo `patrulheiro.py` e insira o código abaixo:

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

        # Coordenadas que passam rente aos obstáculos do labirinto
        self.waypoints = [
            (2.0, 0.0, 0.0),    
            (2.0, 2.0, 1.57),   # <- ATENÇÃO A ESTA COORDENADA
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
            self.get_logger().info(f'Patrulhando Waypoint {self.indice_atual + 1}: alvo em x={x:.2f}, y={y:.2f}')
            self.objetivo_ativo = True
        else:
            self.get_logger().info('Circuito concluído! Reiniciando a patrulha...')
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
            self.get_logger().info(f'>>> Chegamos no destino {self.indice_atual + 1}')
            self.indice_atual += 1
            self.objetivo_ativo = False 

def main(args=None):
    rclpy.init(args=args)
    node = PatrulheiroNav2()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Patrulha interrompida.')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```
*(Lembre-se de adicionar o nó no `setup.py` e executar `colcon build`).*

Abra um Terminal 4 e execute o script:
```bash
ros2 run controle_simulacao patrulheiro
```
Dê o comando de *2D Pose Estimate* no RViz2 para iniciar. 

**Ocorrência do Problema:** Você notará que o robô percorrerá a primeira reta sem problemas, mas **travará completamente** ao tentar ir para o Waypoint 2 `(2.0, 2.0)`, recusando-se a mover as rodas, mesmo com o terminal Python afirmando que o comando está sendo enviado.

---

## 5. Estudo de Caso Teórico: Costmaps e Zonas de Inflação

O robô não travou por causa de um "bug" no código Python, mas sim porque o planejador do Nav2 é programado para priorizar a sobrevivência do hardware. 

Observe o mapa no seu RViz2. Ao redor de cada obstáculo branco (paredes e pilares), o Nav2 desenha auréolas coloridas. Isso é chamado de **Camada de Inflação (Inflation Layer)**. O Nav2 atribui um "custo de travessia" de 0 a 255 para cada pixel do mapa:

1. **Obstáculo Físico (Branco/Preto):** Custo 254. Colisão real.
2. **Zona Ciano (Inscribed/Lethal Cost):** Custo 253. É o tamanho do obstáculo somado à largura do chassi do robô (`robot_radius`). Se o *centro* do robô pisar nessa área ciano, a borda física do robô baterá na parede. 
3. **Zona Roxa (Inflation Cost):** Um gradiente de custo que vai diminuindo de 252 a 1. É uma margem de segurança. O robô *pode* andar aqui, mas o algoritmo tentará evitar.

**O Paradoxo do Waypoint 2:** O Nav2 se recusa estritamente a traçar uma rota cujo destino final caia dentro das zonas Letais (Ciano). A coordenada `(2.0, 2.0)` exigida pelo nosso script cai milimetricamente sobre a zona ciano/roxa escura do pilar central. A matemática do Nav2 prevê uma colisão e, por segurança, aborta a missão.

```json?chameleon
{"component":"LlmGeneratedComponent","props":{"height":"750px","prompt":"Crie um simulador interativo de Costmap Inflation (Mapa de Custos) da robótica.\n\nObjetivo: Demonstrar visualmente como os parâmetros de inflação afetam a navegabilidade ao redor de um obstáculo.\n\nContexto (Data State):\n- Obstáculo central (representando um pilar do labirinto).\n- O ambiente ao redor deve mostrar um grid cartesiano.\n\nLayout e Interação:\n- Painel de Controles com sliders para:\n  1. Raio do Robô (robot_radius): 0.05m a 0.5m. Aumentar isso expande a zona letal (ciano).\n  2. Raio de Inflação (inflation_radius): 0.1m a 2.0m. Controla a extensão total da aura roxa de segurança.\n  3. Fator de Escala de Custo (cost_scaling_factor): 1.0 a 20.0. Controla o quão rápido a aura roxa se dissipa (decaimento exponencial do custo).\n\nVisualização (O Mapa):\n- Desenhe o obstáculo sólido no centro.\n- Renderize a 'Zona Letal' (Inscribed Radius = raio obstáculo + raio robô) em uma cor sólida marcante (ex: ciano claro).\n- Renderize a 'Zona de Inflação' ao redor da Zona Letal usando um gradiente que simule o decaimento do custo (tons de roxo/magenta desvanecendo para transparente).\n- Crie um 'Marcador de Destino' (Waypoint) que o usuário possa arrastar com o mouse pelo mapa.\n\nFeedback Dinâmico:\n- Exiba o Custo exato (0 a 254) no ponto onde o marcador está localizado.\n- Mostre um status claro baseado no marcador: 'Destino Válido (Livre)' ou 'Destino Inválido (Colisão Iminente)'. O destino torna-se inválido se entrar na zona Letal/Ciano.\n- O idioma de toda a interface deve ser Português Brasileiro.","id":"im_6185ddb7218afdf3"}}
```

---

## 6. A Solução: Sintonia Fina (Tuning) com o RQT

Em vez de alterarmos nosso script para desviar do caminho (o que poderia arruinar a missão industrial), vamos reconfigurar o "medo" do robô. Vamos usar a ferramenta **RQT** para alterar os parâmetros do mapa de custo em tempo real, reduzindo a zona de inflação até que a coordenada `(2.0, 2.0)` torne-se um espaço livre.

1. **Abra um Terminal 5** (não esqueça do `export ROS_DOMAIN_ID=XX`).
2. **Inicie o RQT:**
   ```bash
   rqt
   ```
3. No RQT, vá no menu superior e clique em **Plugins** -> **Configuration** -> **Parameter Reconfigure**.
4. Uma lista de nós aparecerá à esquerda. Localize o Costmap Global:
   * Expanda: `/global_costmap` -> `/global_costmap` -> `inflation_layer`.
5. Do lado direito, você verá os parâmetros de segurança:
   * **`inflation_radius`**: (Padrão geralmente é $0.55$). Diminua este valor para algo como **$0.30$**.
   * **`cost_scaling_factor`**: Aumente este valor para algo como **$8.0$**. (Isso fará o custo decair mais rápido, deixando as bordas menos borradas).
6. **Magia em Tempo Real:** Olhe para a tela do seu RViz2. As zonas ciano e roxas ao redor dos pilares encolheram instantaneamente!
7. **Repita para o Mapa Local:** Expanda `/local_costmap` -> `/local_costmap` -> `inflation_layer` na árvore da esquerda e aplique os mesmos valores.

Como a coordenada `(2.0, 2.0)` agora está fora da zona letal, o Nav2 aceitará o destino e o robô **voltará a se mover imediatamente**!

---

## 7. Refatoração: Removendo o "Spam" de Comandos

O robô voltou a andar, mas seu movimento provavelmente está "gaguejando". Esse é o nosso **segundo problema**: a concorrência de comandos. 

No script atual, o `timer_callback` republica a mesma coordenada a cada 2 segundos. No ROS 2, toda vez que o tópico `/goal_pose` recebe uma mensagem, o Nav2 cancela imediatamente a trajetória atual e refaz a matemática do zero. Ao "bombardear" o tópico, forçamos o robô a parar de andar para pensar.

Pare o script atual (`Ctrl+C`) e substitua o código do `patrulheiro.py` por esta versão refatorada, que envia a ordem estritamente uma única vez por etapa:

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

        # As mesmas coordenadas (Agora viáveis graças ao tuning do RQT)
        self.waypoints = [
            (2.0, 0.0, 0.0),    
            (2.0, 2.0, 1.57),   
            (0.0, 2.0, 3.14),   
            (0.0, 0.0, -1.57)   
        ]
        
        self.indice_atual = 0
        self.objetivo_ativo = False # Trava Lógica de Estado
        self.tolerancia_chegada = 0.35  

        self.get_logger().info('Script robusto iniciado. Dê o "2D Pose Estimate"...')

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
            self.get_logger().info(f'Enviando ordem ÚNICA para Waypoint {self.indice_atual + 1}')
            
            # ATIVA A TRAVA: Impede o envio repetido da mesma coordenada
            self.objetivo_ativo = True
        else:
            self.get_logger().info('Circuito concluído! Missão finalizada.')
            self.indice_atual = 0 
            self.objetivo_ativo = False

    def pose_callback(self, msg):
        # Controle de Estado: Só aciona a função de envio se o robô estiver ocioso
        if not self.objetivo_ativo:
            self.enviar_objetivo()
            return

        atual_x = msg.pose.pose.position.x
        atual_y = msg.pose.pose.position.y
        alvo_x, alvo_y, _ = self.waypoints[self.indice_atual]

        distancia = math.sqrt((alvo_x - atual_x)**2 + (alvo_y - atual_y)**2)

        # Checagem de chegada
        if distancia < self.tolerancia_chegada:
            self.get_logger().info(f'>>> Sucesso! Destino {self.indice_atual + 1} alcançado.')
            self.indice_atual += 1
            
            # DESATIVA A TRAVA: Permite o envio do próximo ponto no próximo ciclo
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
Recompile com `colcon build` e rode. O robô agora navegará suavemente pelas zonas ajustadas pelo RQT, garantindo uma patrulha autônoma profissional!

