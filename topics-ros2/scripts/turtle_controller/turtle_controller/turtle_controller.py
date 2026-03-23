#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose


class TurtleControllerNode(Node):
    """
    Nó controlador para a tartaruga no ambiente turtlesim.
    Publica no tópico de velocidade e recebe informações do tópico de posição (pose).
    """

    def __init__(self):
        """
        Inicializa o nó ROS 2 com o nome 'turtle_controller'.
        Cria o publicador para '/turtle1/cmd_vel' e o assinante (subscriber) para '/turtle1/pose'.
        """
        super().__init__("turtle_controller")
        self.cmd_vel_pub_ = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.pose_sub_ = self.create_subscription(Pose, "/turtle1/pose", self.callback_pose, 10)

    def callback_pose(self, pose: Pose):
        """
        Função de callback chamada sempre que uma nova pose da tartaruga é recebida.
        Define e publica as velocidades linear e angular da tartaruga dependendo da sua coordenada 'x'.
        """
        cmd = Twist()
        if pose.x < 5.5:
            # Se a posição em x for menor que 5.5
            cmd.linear.x = 1.0
            cmd.angular.z = 1.0
        else:
            # Se a posição em x for maior ou igual a 5.5
            cmd.linear.x = 2.0
            cmd.angular.z = 2.0
        self.cmd_vel_pub_.publish(cmd)


def main(args=None):
    """
    Ponto de entrada principal do programa.
    Inicializa a comunicação ROS (rclpy), cria a instância do nó
    e o mantém em execução (spin) até que seja interrompido.
    """
    rclpy.init(args=args)
    node = TurtleControllerNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()