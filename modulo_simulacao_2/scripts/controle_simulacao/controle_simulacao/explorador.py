import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import math

class ExploradorReativo(Node):
    def __init__(self):
        super().__init__('explorador_node')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.subscription = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        
        # Margem de segurança
        self.distancia_segura = 0.4  

    def scan_callback(self, msg):
        twist = Twist()
        
        # 1. Criação do Cone de Visão (60 graus frontais)
        visao_esquerda = msg.ranges[0:30]
        visao_direita = msg.ranges[330:360]
        cone_frontal = visao_esquerda + visao_direita
        
        # 2. Limpeza de Dados
        cone_limpo = [dist for dist in cone_frontal if not math.isinf(dist) and not math.isnan(dist)]
        
        # 3. Identifica a menor distância dentro do cone
        if len(cone_limpo) > 0:
            menor_distancia = min(cone_limpo)
        else:
            menor_distancia = 3.5 
        
        # 4. Lógica de Controle Reativo
        if menor_distancia < self.distancia_segura:
            # Obstáculo no cone! Para de andar para frente e gira.
            twist.linear.x = 0.0
            twist.angular.z = 0.8  
            self.get_logger().info(f'Obstáculo a {menor_distancia:.2f}m no cone! Girando...')
        else:
            # Caminho livre! Pode acelerar.
            twist.linear.x = 0.22  
            twist.angular.z = 0.0

        self.publisher_.publish(twist)

    def parar_robo(self):
        """Método dedicado a garantir que o robô pare ao encerrar o nó."""
        msg_parada = Twist()
        msg_parada.linear.x = 0.0
        msg_parada.angular.z = 0.0
        
        # Publica a mensagem de parada
        self.publisher_.publish(msg_parada)
        self.get_logger().info('🛑 Comando de parada de emergência (Ctrl+C) enviado ao /cmd_vel.')


def main(args=None):
    rclpy.init(args=args)
    node = ExploradorReativo()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        # Quando o usuário aperta Ctrl+C, o loop do spin é interrompido
        # e chamamos explicitamente o método de parada antes de destruir o nó.
        node.parar_robo()
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
