# Aula 7: Multiplexação de Comandos e Sistema de Frenagem de Emergência

## 1. Objetivos
* Compreender as limitações de latência do planejador local do Nav2 frente a obstáculos dinâmicos muito rápidos.
* Entender o problema de concorrência de tópicos (quando múltiplos nós tentam controlar os motores simultaneamente).
* Desenvolver um nó **Interceptador / Multiplexador** em Python.
* Utilizar o recurso de *Remapping* (redirecionamento de tópicos) do ROS 2 via linha de comando.

---

## 2. Fundamentação Teórica: A Batalha pelo `/cmd_vel`

Na Aula 6, o Nav2 assumiu o controle do robô, publicando as velocidades calculadas diretamente no tópico `/cmd_vel`. 

Imagine que queremos adicionar um "Freio de Emergência" reativo. Se criarmos um nó que publica velocidade `0.0` no `/cmd_vel` ao ver um obstáculo, e o Nav2 continuar publicando `0.2` no mesmo tópico para tentar avançar, o robô sofrerá de **concorrência (stuttering)**. Os motores receberão comandos conflitantes em frações de segundo, fazendo o robô tremer e agir de forma imprevisível.

### A Solução: O Padrão Interceptador (Multiplexação)
Na indústria, resolvemos isso atribuindo **prioridades**. Para não termos que configurar pacotes complexos de C++ hoje, nós mesmos programaremos um **Multiplexador Simplificado**. 

A arquitetura será a seguinte:
1. Usaremos um comando para "enganar" o Nav2, fazendo-o publicar seus comandos de movimento em um tópico falso chamado `/nav_cmd_vel`.
2. O nosso nó de Emergência vai escutar esse tópico falso (`/nav_cmd_vel`) e também o sensor LiDAR (`/scan`).
3. **A Regra de Ouro:** Se o LiDAR acusar colisão iminente, nosso nó ignora o Nav2 e publica `0.0` no `/cmd_vel` verdadeiro. Se o caminho estiver seguro, nosso nó simplesmente "repassa" a mensagem do Nav2 para o `/cmd_vel` verdadeiro.

---

## 3. Implementação: O Nó de Frenagem de Emergência

No seu pacote `controle_simulacao`, crie um novo arquivo chamado `freio_emergencia.py`.

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import math

class FreioEmergencia(Node):
    def __init__(self):
        super().__init__('freio_emergencia_node')
        
        # 1. Subscriber para o LiDAR (Para detectar perigo)
        self.sub_scan = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        
        # 2. Subscriber para os comandos do Nav2 (Tópico redirecionado)
        self.sub_nav = self.create_subscription(Twist, '/nav_cmd_vel', self.nav_callback, 10)
        
        # 3. Publisher para os motores reais
        self.pub_cmd = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # Variáveis de Estado
        self.menor_distancia = 3.5  # Inicia assumindo caminho livre
        self.distancia_critica = 0.35 # Distância de frenagem absoluta (metros)
        self.freio_ativado = False

    def scan_callback(self, msg):
        """Atualiza a percepção de perigo baseada em um cone frontal."""
        # Extrai um cone frontal de 60 graus (30 esq + 30 dir)
        visao_esquerda = msg.ranges[0:30]
        visao_direita = msg.ranges[330:360]
        cone_frontal = visao_esquerda + visao_direita
        
        # Limpeza (ignora leituras infinitas)
        cone_limpo = [dist for dist in cone_frontal if not math.isinf(dist) and not math.isnan(dist)]
        
        if len(cone_limpo) > 0:
            self.menor_distancia = min(cone_limpo)
        else:
            self.menor_distancia = 3.5

    def nav_callback(self, msg):
        """Intercepta o comando do Nav2, decide a prioridade e publica nos motores."""
        comando_final = Twist()

        # Lógica de Prioridade (Multiplexação)
        if self.menor_distancia < self.distancia_critica:
            # PRIORIDADE 1: FREIO DE EMERGÊNCIA
            comando_final.linear.x = 0.0
            comando_final.angular.z = 0.0
            
            if not self.freio_ativado:
                self.get_logger().error(f'⚠️ COLISÃO EMINENTE ({self.menor_distancia:.2f}m)! Cortando sinal do Nav2.')
                self.freio_ativado = True
        else:
            # PRIORIDADE 2: NAVEGAÇÃO NORMAL (Repassa o comando recebido)
            comando_final = msg
            
            if self.freio_ativado:
                self.get_logger().info('✅ Caminho limpo. Devolvendo controle ao Nav2.')
                self.freio_ativado = False

        # Envia o comando escolhido para os motores reais
        self.pub_cmd.publish(comando_final)


def main(args=None):
    rclpy.init(args=args)
    node = FreioEmergencia()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        # Garante parada ao encerrar
        parada = Twist()
        node.pub_cmd.publish(parada)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Lembrete de Compilação:** 1. Adicione `'freio_emergencia = controle_simulacao.freio_emergencia:main'` no `setup.py`.
2. Compile o pacote (`colcon build`) e atualize o ambiente (`source install/setup.bash`).

---

## 4. Ordem de Execução e o Truque do Remap

Para que nosso plano funcione, precisamos isolar as instâncias. **Atenção especial ao Terminal 3.**

1. **Terminal 1 (Gazebo):**
   ```bash
   export TURTLEBOT3_MODEL=waffle
   ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
   ```

2. **Terminal 2 (Nosso Freio de Emergência):**
   Inicie o seu nó interceptador primeiro. Ele ficará aguardando dados.
   ```bash
   ros2 run controle_simulacao freio_emergencia
   ```

3. **Terminal 3 (Navegação com Remap - CRÍTICO):**
   Ao lançar o Nav2, adicionaremos o argumento `--ros-args --remap` para obrigar toda a pilha de navegação a despejar os comandos de velocidade no tópico `/nav_cmd_vel` em vez do padrão.
   ```bash
   export TURTLEBOT3_MODEL=waffle
   ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True map:=$HOME/mapa_lab.yaml --ros-args --remap cmd_vel:=/nav_cmd_vel
   ```

4. **Terminal 4 (Patrulheiro da Aula 6):**
   Execute o script que vocês criaram na aula passada para que o robô comece a patrulhar os waypoints automaticamente.
   ```bash
   ros2 run controle_simulacao patrulheiro
   ```

---

## 5. Testando o Sistema na Prática

1. Configure a **Estimativa de Pose (AMCL)** no RViz2 como de costume.
2. O robô começará a patrulhar os pontos programados.
3. **O Teste Físico:** Vá até a janela do simulador **Gazebo**. Selecione um objeto (como uma caixa de papelão ou um cubo) e coloque-o **abruptamente** bem na frente do robô em movimento.
4. **Observação:** O planejador local do Nav2 (DWA) não terá tempo hábil de recalcular a rota (ele demora algumas frações de segundo para atualizar o Costmap). No entanto, o seu **Freio de Emergência** (que roda a 10Hz focado apenas no laser frontal) reagirá instantaneamente, parando o robô antes da batida e emitindo o log vermelho de erro no Terminal 2.

---

## 6. Desafio Analítico para o Relatório

Para conectar esta arquitetura de software com a teoria de Sistemas de Tempo Real:

1. **Diagrama de Blocos:** Desenhe (ou descreva textualmente) o novo fluxo de dados (Pipeline) entre os seguintes nós e tópicos: `Nav2`, `Patrulheiro`, `Freio de Emergência`, `/goal_pose`, `/nav_cmd_vel`, `/scan`, `/cmd_vel` e `Controlador do Robô`.
2. **Distância de Frenagem Dinâmica:** No nosso código, a `distancia_critica` foi fixada (Hardcoded) em $0.35$ metros. Do ponto de vista da física clássica (Inércia e Atrito), por que uma distância de frenagem estática é perigosa em um veículo real? Como você alteraria a equação no Python para que a distância crítica fosse calculada *dinamicamente* com base na velocidade linear atual que o Nav2 está tentando impor?
3. **Falha Silenciosa:** Se o nó `freio_emergencia` "travar" ou for encerrado acidentalmente, o que acontecerá com o robô (considerando a configuração atual onde o Nav2 publica em `/nav_cmd_vel`)? Esse comportamento é seguro (Fail-Safe)? Explique.