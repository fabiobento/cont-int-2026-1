#!/usr/bin/env python3

"""
Módulo responsável por gravar e visualizar os estados das juntas (posições e velocidades)
do ambiente CartPole, assinando o tópico '/joint_states' do ROS 2.
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import matplotlib.pyplot as plt
import time
import os
import math

def bound_angle(angle):
    """
    Normaliza o ângulo para mantê-lo no intervalo entre -pi e pi.
    
    Args:
        angle (float): O ângulo em radianos.
        
    Returns:
        float: O ângulo normalizado.
    """
    # Normaliza o ângulo entre -pi e pi
    bounded_angle = (angle + math.pi) % (2 * math.pi) - math.pi
    return bounded_angle


class JointStateRecorder(Node):
    """
    Nó do ROS 2 para gravar dados de estado das juntas e, opcionalmente, 
    salvá-los em um arquivo ou gerar gráficos.
    """
    def __init__(self):
        super().__init__('joint_state_recorder')
        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10)
        self.joint_positions = []
        self.joint_velocity = []
        self.timestamps = []
        self.timestamps_vel = []

    def joint_state_callback(self, msg):
        """
        Callback acionado ao receber mensagens no tópico '/joint_states'.
        Armazena posições, velocidades e os tempos em que foram recebidos.
        """
        # Adiciona as posições e as marcações de tempo (timestamps)
        self.joint_positions.append(msg.position)
        self.timestamps.append(self.get_clock().now().seconds_nanoseconds()[0])
        self.get_logger().info(f"Gravando posições das juntas: {msg.position}")

        # Adiciona as velocidades e as marcações de tempo correspondentes
        self.joint_velocity.append(msg.velocity)
        self.timestamps_vel.append(self.get_clock().now().seconds_nanoseconds()[0])


    def save_data(self):
        """
        Salva as posições das juntas coletadas em um arquivo de texto.
        """
        # Salva as posições das juntas coletadas em um arquivo
        data_dir = os.path.join(os.getcwd(), 'joint_states_data')
        os.makedirs(data_dir, exist_ok=True)
        file_path = os.path.join(data_dir, f'joint_positions_{int(time.time())}.txt')
        
        with open(file_path, 'w') as file:
            for t, positions in zip(self.timestamps, self.joint_positions):
                file.write(f"{t}, {', '.join(map(str, positions))}\n")
        
        self.get_logger().info(f"Dados de posição das juntas salvos em {file_path}")
        return file_path

    def plot_data(self):
        """
        Gera gráficos exibindo as posições e velocidades do carro e da haste ao longo do tempo.
        """
        # Assumindo que estamos interessados na posição da primeira junta (carro) para simplificar
        joint_positions_array = [pos[0] for pos in self.joint_positions]  # Ajuste o índice para outras juntas
        plt.figure()
        plt.plot(self.timestamps, joint_positions_array)
        plt.title('Posição do carro')
        plt.xlabel('Tempo (s)')
        plt.ylabel('Posição (m)')
        plt.grid(True)
        #plt.show()

        # Posição da segunda junta (haste)
        joint_positions_array = [pos[1] for pos in self.joint_positions]  # Ajuste o índice para outras juntas
        plt.figure()
        plt.plot(self.timestamps, joint_positions_array)
        plt.title('Orientação da haste')
        plt.xlabel('Tempo (s)')
        plt.ylabel('Posição (rad)')
        plt.grid(True)
        
        # Velocidade da primeira junta (carro)
        joint_velocity_array = [vel[0] for vel in self.joint_velocity]  # Ajuste o índice para outras juntas
        plt.figure()
        plt.plot(self.timestamps_vel, joint_velocity_array)
        plt.title('Velocidade do carro')
        plt.xlabel('Tempo (s)')
        plt.ylabel('Velocidade (m/s)')
        plt.grid(True)
        

        # Velocidade da segunda junta (haste)
        joint_velocity_array = [vel[1] for vel in self.joint_velocity]  # Ajuste o índice para outras juntas
        plt.figure()
        plt.plot(self.timestamps_vel, joint_velocity_array)
        plt.title('Velocidade da haste')
        plt.xlabel('Tempo (s)')
        plt.ylabel('Velocidade de rotação (rad/s)')
        plt.grid(True)
        plt.show()
        '''

        '''
def main(args=None):
    """
    Função principal. Inicializa o rclpy, instancia o gravador e mantém
    o nó ativo. Quando interrompido, gera os gráficos.
    """
    rclpy.init(args=args)
    joint_state_recorder = JointStateRecorder()

    try:
        # Mantém o nó rodando (spin) até ser interrompido manualmente
        rclpy.spin(joint_state_recorder)
    except KeyboardInterrupt:
        joint_state_recorder.get_logger().info('Salvando e gerando gráficos...')
        #joint_state_recorder.save_data()
        joint_state_recorder.plot_data()
    finally:
        joint_state_recorder.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
