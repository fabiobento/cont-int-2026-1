import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray, Bool
from sensor_msgs.msg import JointState
from threading import Thread
import math

def bound_angle(angle):
    bounded_angle = (angle + math.pi) % (2 * math.pi) - math.pi
    return bounded_angle

class CartPoleReset(Node):
    def __init__(self):
        super().__init__('yolo_node')
        self.js_sub = self.create_subscription(JointState, "/joint_states", self.js_cb, 10)
        self.cartpole_eff_pub = self.create_publisher(Float64MultiArray, "/effort_control/commands", 10)
        self.system_ready_pub = self.create_publisher(Bool, "/cartpole/ready", 10)
        self.cartpole__reset_sub = self.create_subscription(Bool, "/cartpole/reset", self.reset, 10)
        self.stick_eff_pub = self.create_publisher(Float64MultiArray, "/stick_effort_control/commands", 10)
        self.timer = self.create_timer(0.1, self.publish_system_ready)
        self.reset = False
        self.js_ready = False
        self.js = None
        self.system_ready = Bool()
        self.system_ready.data = True
    
    def main_loop(self): 
       
        rate = self.create_rate(2)
        while not self.js_ready:
            rate.sleep()   
        while rclpy.ok():

            if( self.reset == True):
                self.system_ready.data = False
                self.system_ready_pub.publish(self.system_ready)
              
                rate2 = self.create_rate(100)
                
                self.reset = False
         
                cmd = Float64MultiArray()  
                stick_tau_cmd = Float64MultiArray()                
              
                k = 0.8
                k2 = 0.2
                k_stick = 0.1
                k2_stick = 0.05
                stick_e = 0.0
                prev_stick_e = 0.0
                stick_derivative = 0.0
                
                cart_e = 0 
                prev_cart_e = 0
                cart_e_derivative = 0
                cart_e = self.js.position[0]
                prev_cart_e = 0
                
                stick_js = bound_angle(self.js.position[1])
                
                while ( (math.fabs( stick_js) > 0.05) or (math.fabs(self.js.velocity[0]) > 0.01) ) :
                     
                    cart_e = (self.js.position[0])
                    cart_e_derivative = (cart_e - prev_cart_e) / (1.0/100.0)
                    cart_c = k*cart_e + k2*cart_e_derivative
                    cmd.data = [-cart_c]



                    stick_js = bound_angle(self.js.position[1])
                    
                    stick_e = math.fabs( stick_js )
                    stick_derivative = (stick_e - prev_stick_e) / (1.0/100.0)

                    tau = k_stick*stick_e + k2_stick*stick_derivative

                    if ( stick_js > 0 ):
                        tau = -tau
                    
                    stick_tau_cmd.data = [tau]
                    
                    self.cartpole_eff_pub.publish(cmd)
                    self.stick_eff_pub.publish(stick_tau_cmd)
                    prev_stick_e = stick_e
                    prev_cart_e = cart_e

                    rate2.sleep()

                self.system_ready.data = True

            rate.sleep()


    def reset(self, msg):
        self.reset = True

    def publish_system_ready(self):
        self.system_ready_pub.publish(self.system_ready)

    def js_cb(self, msg):
        self.js = msg
        self.js_ready = True

    def run( self ):
        main_loop_thread = Thread(target = self.main_loop, args = ())
        main_loop_thread.start()
        rclpy.spin(self)

def main(args=None):
    rclpy.init(args=args)

    node = CartPoleReset()
    node.run()

if __name__ == '__main__':
    main()
