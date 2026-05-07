
# Aula 7: Treinando o lab_bot com PPO


## 1. Instalação de Dependências
Garanta que a bancada possui as bibliotecas de Inteligência Artificial instaladas:
```bash
pip install -qU gymnasium stable_baselines3
```

## 2. O Ambiente Customizado Gym-ROS (`lab_bot_env.py`)

No seu pacote `lab_bot`, crie o ficheiro que fará a tradução entre a simulação do Gazebo e a Rede Neural. Este é o coração da integração.

```python
import gymnasium as gym
from gymnasium import spaces
import numpy as np
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
import math

class LabBotRLEnv(gym.Env, Node):
    """Ambiente Customizado que segue a interface OpenAI Gym, encapsulando um Nó ROS 2."""
    
    def __init__(self):
        Node.__init__(self, 'lab_bot_rl_env')
        gym.Env.__init__(self)

        # Configurações do Robô e Alvo
        self.goal_x = 2.0
        self.goal_y = 2.0
        self.max_steps = 500
        self.current_step = 0
        
        # Variáveis de Estado
        self.laser_ranges = np.ones(20) * 10.0 # 20 raios resumidos
        self.robot_x = 0.0
        self.robot_y = 0.0
        self.robot_theta = 0.0
        
        # ROS 2 Pub/Sub
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.odom_sub = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)

        # Espaços do Gym
        # Ações: 0=Frente, 1=Esquerda, 2=Direita
        self.action_space = spaces.Discrete(3)
        
        # Observações: 20 raios laser + dist_alvo + angulo_alvo = 22 valores
        high = np.inf * np.ones(22, dtype=np.float32)
        self.observation_space = spaces.Box(-high, high, dtype=np.float32)

    def scan_callback(self, msg):
        # Reduz os 360 raios para 20 raios representativos (subamostragem)
        ranges = np.array(msg.ranges)
        ranges[np.isinf(ranges)] = 10.0
        ranges[np.isnan(ranges)] = 10.0
        indices = np.linspace(0, len(ranges)-1, 20, dtype=int)
        self.laser_ranges = ranges[indices]

    def odom_callback(self, msg):
        self.robot_x = msg.pose.pose.position.x
        self.robot_y = msg.pose.pose.position.y
        # Conversão simplificada de quaternion para Euler (Z)
        q = msg.pose.pose.orientation
        self.robot_theta = math.atan2(2.0*(q.w*q.z + q.x*q.y), 1.0 - 2.0*(q.y*q.y + q.z*q.z))

    def get_observation(self):
        # Lê a fila de mensagens do ROS 2 para atualizar as variáveis
        rclpy.spin_once(self, timeout_sec=0.01)
        
        dist_alvo = math.sqrt((self.goal_x - self.robot_x)**2 + (self.goal_y - self.robot_y)**2)
        angulo_alvo = math.atan2(self.goal_y - self.robot_y, self.goal_x - self.robot_x) - self.robot_theta
        
        # Normaliza o ângulo entre -pi e pi
        angulo_alvo = (angulo_alvo + math.pi) % (2 * math.pi) - math.pi
        
        obs = np.concatenate([self.laser_ranges, [dist_alvo, angulo_alvo]]).astype(np.float32)
        return obs, dist_alvo

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.current_step = 0
        
        # Num ambiente real, enviaríamos um serviço ao Gazebo para teletransportar o robô para a origem.
        # Aqui assumimos que o robô está na posição inicial.
        
        # Para o robô
        msg = Twist()
        self.cmd_pub.publish(msg)
        
        obs, _ = self.get_observation()
        return obs, {}

    def step(self, action):
        self.current_step += 1
        
        # 1. Executa a Ação
        msg = Twist()
        msg.linear.x = 0.2 # Sempre avança ligeiramente
        if action == 1:
            msg.angular.z = 0.5  # Esquerda
        elif action == 2:
            msg.angular.z = -0.5 # Direita
            
        self.cmd_pub.publish(msg)
        
        # 2. Aguarda um momento para a física atuar e lê as observações
        obs, dist_alvo = self.get_observation()
        
        # 3. Calcula a Recompensa
        reward = 0.0
        done = False
        truncated = False
        
        min_laser = np.min(self.laser_ranges)
        
        if min_laser < 0.15: # Bateu na parede
            reward = -50.0
            done = True
        elif dist_alvo < 0.3: # Chegou ao alvo
            reward = 100.0
            done = True
        else:
            # Recompensa por se aproximar (baseada na distância inversa)
            reward = 1.0 / (dist_alvo + 0.1)
            
        if self.current_step >= self.max_steps:
            truncated = True

        return obs, reward, done, truncated, {}

```

## 3. O Script de Treino (`treinar_rl.py`)

Agora que temos o ambiente, aplicar o algoritmo PPO é extremamente simples graças à `Stable-Baselines3`.

```python
import rclpy
from stable_baselines3 import PPO
from lab_bot_env import LabBotRLEnv # Importa a classe que criamos

def main():
    rclpy.init()
    
    # 1. Instancia o ambiente ROS-Gym
    env = LabBotRLEnv()
    
    # 2. Configura a Rede Neural (MlpPolicy para dados numéricos em vetor)
    print("A iniciar o Cérebro do Robô (PPO)...")
    modelo = PPO("MlpPolicy", env, verbose=1, tensorboard_log="./ppo_nav_tensorboard/")
    
    # 3. Inicia o treino
    # Num laboratório real, isto seria na ordem dos 100.000 a 1.000.000 de passos.
    try:
        modelo.learn(total_timesteps=10000, progress_bar=True)
        modelo.save("cerebro_lab_bot")
        print("Treino concluído e modelo guardado!")
    except KeyboardInterrupt:
        print("Treino interrompido pelo utilizador. A guardar progresso...")
        modelo.save("cerebro_lab_bot_interrompido")
    finally:
        env.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## 4. Executando o Laboratório

Para rodar este treino de forma impecável, execute os comandos isolando o domínio de rede da sua bancada:

1. **Terminal 1 (Física):** Inicie o Gazebo com o robô num labirinto com paredes.
```bash
export ROS_DOMAIN_ID=30
ros2 launch lab_bot simulacao.launch.py
```


2. **Terminal 2 (Sentidos):** Rode a ponte (Bridge) para traduzir o laser e os motores.
```bash
export ROS_DOMAIN_ID=30
ros2 run ros_gz_bridge parameter_bridge /cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist /scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan /odom@nav_msgs/msg/Odometry@gz.msgs.Odometry
```


3. **Terminal 3 (Cérebro):** Inicie o script de treino em Python.
```bash
export ROS_DOMAIN_ID=30
python3 treinar_rl.py
```



## 5. Troubleshooting (Sintonia Fina do Reset)

* **Atenção ao Reset:** No código acima, simplificamos a função `reset()`. Numa simulação contínua, quando o robô bate na parede, ele precisa de ser "teletransportado" de volta à origem. Para implementar isso de forma robusta no ROS 2 Jazzy, precisaria de adicionar um `Service Client` na função `reset()` que chame o serviço `/world/empty/set_pose` do Gazebo Harmonic. Caso contrário, os você precisaria reiniciar a simulação do Gazebo manualmente a cada colisão ou utilizar as paredes curtas para que o robô deslize e continue tentando navegar.
