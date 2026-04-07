import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class CircularMotion(Node):
    def __init__(self):
        super().__init__('circular_motion_node')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        timer_period = 0.1  # 10 Hz
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.get_logger().info('Executando trajetória circular...')

    def timer_callback(self):
        msg = Twist()
        # v = 0.15 m/s | w = 0.4 rad/s
        msg.linear.x = 0.15
        msg.angular.z = 0.4 
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = CircularMotion()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Comando de parada enviado.')
        node.publisher_.publish(Twist()) # Stop
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()