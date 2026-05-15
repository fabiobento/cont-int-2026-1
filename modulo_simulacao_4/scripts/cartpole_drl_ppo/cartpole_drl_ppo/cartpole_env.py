"""
Ambiente Customizado Gymnasium para o Pêndulo Invertido (CartPole) com ROS 2 e Gazebo.

Este módulo implementa a classe de ambiente que atua como ponte entre a 
biblioteca de Aprendizado por Reforço (como Stable Baselines3) e o simulador 
físico (Ignition/Harmonic Gazebo) gerenciado pelo ROS 2.
"""

import rclpy
import gymnasium as gym
from gymnasium import spaces
import numpy as np
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import Bool
from threading import Thread
import threading
import time
import math

def bound_angle(angle):
    """
    Normaliza o ângulo fornecido para mantê-lo estritamente no intervalo [-π, π].

    Isso é imporatnte para a Rede Neural, pois evita que a observação do ângulo 
    cresça infinitamente caso o pêndulo dê voltas completas no próprio eixo.

    Argumentos:
        angle (float): O ângulo bruto em radianos lido do sensor.

    Retorna:
        float: O ângulo normalizado no intervalo [-π, π].
    """
    bounded_angle = (angle + math.pi) % (2 * math.pi) - math.pi
    return bounded_angle


class CartPoleROS2Env(gym.Env):
    """
    Ambiente Gymnasium integrado com ROS 2 para controle do CartPole.

    Esta classe empacota a comunicação assíncrona do ROS 2 (tópicos e callbacks)
    no padrão síncrono de passos (steps) esperado pelos algoritmos de DRL.

    Atributos:
        action_space (gymnasium.spaces.Box): Espaço contínuo de ações definindo a força a ser aplicada no carro.
        observation_space (gymnasium.spaces.Box): Espaço contínuo do estado do robô.
        node (rclpy.node.Node): Nó embutido do ROS 2 para comunicação.
    """
    
    def __init__(self):
        """
        Inicializa o espaço de ação, espaço de observação e a comunicação ROS 2.
        """
        super(CartPoleROS2Env, self).__init__()
        
        # Define o espaço de ações: um valor contínuo (esforço/força em Newtons)
        # Os limites definidos são de -15.0 N a 15.0 N para a base prismática.
        self.action_space = spaces.Box(low=-15.0, high=15.0, shape=(1,), dtype=np.float32)
        
        # Limites para o espaço de observações:
        # [posição_carro (m), velocidade_carro (m/s), ângulo_haste (rad), velocidade_angular_haste (rad/s)]
        high = np.array([5.0, 1.0, math.pi, 8.5], dtype=np.float32)
        self.observation_space = spaces.Box(-high, high, dtype=np.float32)
        
        # Inicialização do nó interno do ROS 2
        rclpy.init(args=None)
        self.node = rclpy.create_node('cartpole_gym_env')
        
        # Configuração dos Publishers (Comandos) e Subscribers (Sensores e Status)
        self.cartpole_eff_pub = self.node.create_publisher(Float64MultiArray, "/effort_control/commands", 10)
        self.joint_state_sub = self.node.create_subscription(JointState, '/joint_states', self.joint_state_callback, 10 )
        self.cartpole_reset_pub = self.node.create_publisher(Bool, "/cartpole/reset", 10)
        self.system_ready_sub = self.node.create_subscription(Bool, '/cartpole/ready', self.system_ready_cb, 10 )

        # Inicialização das variáveis de estado interno
        self.current_observation = np.zeros(4, dtype=np.float32)
        self.state_received = False
        self.system_ready = False

        # Configura um executor do ROS 2 em uma thread separada em background.
        # Isso permite que os callbacks de sensores continuem atualizando os 
        # dados assincronamente enquanto o algoritmo de IA realiza os cálculos.
        self.executor = rclpy.executors.SingleThreadedExecutor()
        self.executor.add_node(self.node)
        self.spin_thread = threading.Thread(target=self.executor.spin, daemon=True)
        self.spin_thread.start()

    def system_ready_cb(self, msg):
        """
        Callback acionado pelo nó de reset indicando a prontidão da simulação física.

        Argumentos:
            msg (std_msgs.msg.Bool): True se o pêndulo estiver posicionado e estabilizado.
        """
        self.system_ready = msg.data

    def joint_state_callback(self, msg):
        """
        Callback de leitura dos encoders (sensores de junta) do simulador Gazebo.

        Atualiza o vetor de observação da IA sempre que o ROS 2 publica novos dados.

        Argumentos:
            msg (sensor_msgs.msg.JointState): Mensagem contendo posição e velocidade atual.
        """
        try:
            # Constrói o vetor de observação processando a cinemática básica
            self.current_observation = np.array([
                msg.position[0],               # Posição linear do carrinho
                msg.velocity[0],               # Velocidade linear do carrinho
                bound_angle(msg.position[1]),  # Ângulo normalizado da haste
                msg.velocity[1]                # Velocidade angular da haste
            ], dtype=np.float32)
            
            self.state_received = True
        except ValueError:
            # Ignora falhas de leitura temporárias antes dos controladores inicializarem completamente
            pass
    
    def step(self, action):
        """
        Aplica a força calculada pela IA ao robô e avança um passo no tempo.

        Argumentos:
            action (numpy.ndarray): O vetor de ação gerado pela política do agente (esforço).

        Retorna:
            tuple: Contendo:
                - obs (numpy.ndarray): O novo estado após aplicar a ação.
                - reward (float): A recompensa obtida neste passo de tempo.
                - done (bool): Verdadeiro se o episódio falhou (queda) e precisa terminar.
                - truncated (bool): Verdadeiro se o tempo limite do episódio foi atingido.
                - info (dict): Dicionário de informações adicionais (vazio por padrão).
        """
        # Trava de segurança: Aguarda o primeiro dado de sensor antes de agir
        if not self.state_received:
            time.sleep(0.01)
            return self.current_observation, 0.0, False, False, {}
        
        # Empacota o esforço gerado pela Rede Neural e envia para o ROS 2 Control
        eff_msg = Float64MultiArray()
        eff_msg.data = [float(action[0])]
        self.cartpole_eff_pub.publish(eff_msg)
        
        # Aguarda a física do Gazebo processar a força (simulando a taxa de 100Hz de controle)
        time.sleep(0.01)  
        
        obs = self.current_observation.copy()
        reward = 1.0  # Recompensa padrão por manter o pêndulo em pé neste instante
                
        # Condições de falha (Término do Episódio):
        # 1. Carro saiu da pista útil (-2m a 2m)
        # 2. Haste inclinou mais que 45 graus (pi/4)
        # 3. Velocidade angular excessiva (instabilidade iminente)
        # 4. Velocidade linear excessiva (risco de bater no fim do trilho)
        done = bool(
            obs[0] < -2 or obs[0] > 2 or
            obs[2] < -math.pi/4 or obs[2] > math.pi/4 or 
            math.fabs( obs[3] > 0.3 ) or 
            math.fabs( obs[1] > 1.0 )
        )

        # Modulação de Recompensa (Shaping): Penaliza severamente comportamentos oscilatórios
        # ou violentos do carrinho para forçar um aprendizado mais suave e seguro.
        if( math.fabs( obs[1] > 1.0 ) ): 
           reward = -10
        
        truncated = False
        info = {}
        
        return obs, reward, done, truncated, info
    
    def reset(self, seed=None, options=None):
        """
        Reinicia fisicamente o ambiente para iniciar um novo episódio de treinamento.

        Esta função se comunica com o nó auxiliar `cartpole_reset` para aplicar
        os PIDs virtuais que levantam o pêndulo de volta à posição inicial no simulador.

        Argumentos:
            seed (int, opcional): Semente de aleatoriedade para reprodutibilidade.
            options (dict, opcional): Opções extras de reset.

        Retorna:
            tuple: Contendo a observação inicial após o reset e o dicionário de informações.
        """
        if seed is not None:
             np.random.seed(seed)
            
        # Dispara o comando de reset pela rede do laboratório
        reset_data = Bool()
        reset_data.data = True
        self.cartpole_reset_pub.publish( reset_data )
        time.sleep(0.5) # Tempo de tolerância para o nó de reset assumir o controle

        # Bloqueia o avanço da Inteligência Artificial até que o braço invisível 
        # (nó de reset) confirme que posicionou o pêndulo no centro e parou de tremer.
        while( not self.system_ready ):
            time.sleep(0.001)

        info = {}
        return self.current_observation.copy(), info
    

    def close(self):
        """
        Desliga ordenadamente o ambiente, encerrando as threads em background e
        fechando o nó do ROS 2 para liberar os recursos do sistema operacional.
        """
        self.executor.shutdown()
        self.node.destroy_node()
        rclpy.shutdown()