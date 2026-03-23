#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class ControleAbertoNode(Node):
    def __init__(self):
        super().__init__("controle_aberto")
        
        # Parâmetros de Tempo Discreto
        self.Ts_ = 0.5  # Tempo de Amostragem (Segundos)
        self.k_ = 0     # Instante atual (tick)
        
        # Caixa Preta (Atuador)
        self.pub_motor = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        
        # O Timer é o "Clock" do nosso controlador
        self.timer_ = self.create_timer(self.Ts_, self.loop_controle)
        
        # Controle de Estado (0 = Andando, 1 = Girando)
        self.estado_ = 0 
        
        self.get_logger().info("Controlador de Malha Aberta Iniciado!")

    def loop_controle(self):
        msg = Twist()
        
        # ESTADO 0: Andar para frente por 2 metros (v = 1.0 m/s)
        # N = 2.0 / (1.0 * 0.5) = 4 ticks
        if self.estado_ == 0:
            msg.linear.x = 1.0
            msg.angular.z = 0.0
            self.k_ += 1
            self.get_logger().info(f"Andando... Tick {self.k_}/4")
            
            if self.k_ >= 4:
                self.estado_ = 1  # Muda para rotação
                self.k_ = 0       # Zera o contador k

        ## TRECHO PARA O DESAFIO DO TRIANGULO EQUILÁTERO (120 graus)
        # ESTADO 1: Girar 120 graus (aprox. 2.094 rad)
        # Escolhemos N = 4 ticks. Então w = 1.047 rad/s
        elif self.estado_ == 1:
            msg.linear.x = 0.0
            msg.angular.z = 1.047  # Nova velocidade angular
            self.k_ += 1
            self.get_logger().info(f"Girando 120 graus... Tick {self.k_}/4")
            
            if self.k_ >= 4: # Novo limite de ticks
                self.estado_ = 0  # Volta a andar
                self.k_ = 0

        '''
        # ESTADO 1: Girar 90 graus (aprox. 1.57 rad) com w = 1.57 rad/s
        # N = 1.57 / (1.57 * 0.5) = 2 ticks
        elif self.estado_ == 1:
            msg.linear.x = 0.0
            msg.angular.z = 1.57 
            self.k_ += 1
            self.get_logger().info(f"Girando... Tick {self.k_}/2")
            
            if self.k_ >= 2:
                self.estado_ = 0  # Volta a andar
                self.k_ = 0
        '''

        # Aplica o esforço de controle na planta
        self.pub_motor.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = ControleAbertoNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
