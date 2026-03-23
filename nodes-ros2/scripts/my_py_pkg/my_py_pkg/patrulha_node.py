#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist # Interface para comandos de velocidade 

class PatrulhaNode(Node):
    def __init__(self):
        super().__init__("patrulha_node") # Nome que aparecerá no 'ros2 node list' 
        self.publisher_ = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.timer_ = self.create_timer(2.0, self.executar_ronda) # Loop de controle temporal 
        self.fase_ = 0
        self.get_logger().info("Iniciando a ronda da tartaruga IFES...")

    def executar_ronda(self):
        msg = Twist()
        if self.fase_ % 2 == 0:
            msg.linear.x = 2.0 # Avança 
            self.get_logger().info("Status: Avançando!")
        else:
            msg.angular.z = 1.57 # Vira 90 graus 
            self.get_logger().info("Status: Virando a esquina...")
        self.publisher_.publish(msg)
        self.fase_ += 1

def main(args=None):
    rclpy.init(args=args)
    node = PatrulhaNode()
    rclpy.spin(node) # Mantém o robô "escutando" e o timer ativo 
    rclpy.shutdown()

if __name__ == "__main__":
    main()