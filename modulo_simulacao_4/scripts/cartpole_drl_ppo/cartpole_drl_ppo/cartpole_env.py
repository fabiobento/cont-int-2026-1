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
    Normaliza o ângulo para mantê-lo no intervalo entre -pi e pi.
    """
    bounded_angle = (angle + math.pi) % (2 * math.pi) - math.pi
    return bounded_angle


class CartPoleROS2Env(gym.Env):
    """Ambiente personalizado do CartPole integrado com ROS 2 e Gazebo."""
    
    def __init__(self):
        super(CartPoleROS2Env, self).__init__()
        
        # Define o espaço de ações: um valor contínuo (esforço) entre -15.0 e 15.0
        self.action_space = spaces.Box(low=-15.0, high=15.0, shape=(1,), dtype=np.float32)
        
        # Limites para o espaço de observações: [posição_carro, velocidade_carro, ângulo_haste, velocidade_angular_haste]
        high = np.array([5.0, 1.0, math.pi, 8.5], dtype=np.float32)
        self.observation_space = spaces.Box(-high, high, dtype=np.float32)
        
        # Inicializa o ROS 2 e cria o nó do ambiente
        rclpy.init(args=None)
        self.node = rclpy.create_node('cartpole_gym_env')
        
        # Publishers e Subscribers do ROS 2
        self.cartpole_eff_pub = self.node.create_publisher(Float64MultiArray, "/effort_control/commands", 10)
        self.joint_state_sub = self.node.create_subscription(JointState, '/joint_states', self.joint_state_callback, 10 )
        self.current_observation = np.zeros(4, dtype=np.float32)
        self.state_received = False
        self.cartpole_reset_pub = self.node.create_publisher(Bool, "/cartpole/reset", 10)
        self.system_ready_sub = self.node.create_subscription(Bool, '/cartpole/ready', self.system_ready_cb, 10 )

        # Estado inicial
        self.current_observation = np.zeros(4, dtype=np.float32)
        self.state_received = False
        self.system_ready = False

        # Configura um executor em uma thread separada para processar os callbacks do ROS 2
        self.executor = rclpy.executors.SingleThreadedExecutor()
        self.executor.add_node(self.node)
        self.spin_thread = threading.Thread(target=self.executor.spin, daemon=True)
        self.spin_thread.start()
        self.system_ready = False

    def system_ready_cb(self, msg):
        """Callback acionado quando o sistema indica que o ambiente Gazebo/ROS está pronto."""
        self.system_ready = msg.data

    def joint_state_callback(self, msg):
        """Callback que atualiza as observações atuais a partir dos estados das juntas do robô."""
        try:
            # Monta o vetor de observação: posição e velocidade do carro, ângulo e velocidade da haste
            self.current_observation = np.array([
                msg.position[0],
                msg.velocity[0],
                bound_angle(msg.position[1]), # Normaliza o ângulo para -pi a pi
                msg.velocity[1]
            ], dtype=np.float32)
            
            self.state_received = True
        except ValueError:
            # Tratamento caso os nomes das juntas não sejam encontrados
            pass
    
    def step(self, action):
        """
        Aplica uma ação no ambiente e retorna as novas observações e a recompensa.
        """
        if not self.state_received:
            # Se nenhum estado foi recebido ainda, apenas aguarda
            time.sleep(0.01)
            return self.current_observation, 0.0, False, False, {}
        
        # Prepara e publica a mensagem de esforço (ação)
        eff_msg = Float64MultiArray()
        eff_msg.data = [float(action[0])]
        self.cartpole_eff_pub.publish(eff_msg)
        time.sleep(0.01)  
        
        obs = self.current_observation.copy()
        reward = 1.0  
                
        # Condições de término (falha): carro sai dos limites ou haste tomba muito
        done = bool(
            obs[0] < -2 or obs[0] > 2 or
            obs[2] < -math.pi/4 or obs[2] > math.pi/4 or 
            math.fabs( obs[3] > 0.3 ) or 
            math.fabs( obs[1] > 1.0 )
        )

        # Penalidade caso a velocidade do carro ultrapasse o limite aceitável
        if( math.fabs( obs[1] > 1.0 ) ): 
           reward = -10
        
        truncated = False  # Pode ser configurado caso haja limite máximo de tempo/passos
        info = {}
        
        return obs, reward, done, truncated, info
    
    def reset(self, seed=None, options=None):
        """
        Reinicia o ambiente para o estado inicial, pedindo ao Gazebo/ROS para resetar a simulação.
        """
        if seed is not None:
             np.random.seed(seed)
            
        # Publica a flag de reset no tópico correspondente
        reset_data = Bool()
        reset_data.data = True
        self.cartpole_reset_pub.publish( reset_data )
        time.sleep(0.5)

        # Bloqueia até que o ambiente confirme que está pronto para prosseguir
        while( not self.system_ready ):
            time.sleep(0.001)

        info = {}
        return self.current_observation, info
    

    def close(self):
        """
        Encerra o ambiente, parando o executor e destruindo o nó do ROS 2.
        """
        self.executor.shutdown()
        self.node.destroy_node()
        rclpy.shutdown()


