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
    # Normalize the angle between -pi and pi
    bounded_angle = (angle + math.pi) % (2 * math.pi) - math.pi
    return bounded_angle


class CartPoleROS2Env(gym.Env):
    """Custom CartPole environment integrated with ROS 2 and Gazebo."""
    
    def __init__(self):
        super(CartPoleROS2Env, self).__init__()
        self.action_space = spaces.Box(low=-15.0, high=15.0, shape=(1,), dtype=np.float32)
        high = np.array([5.0, 1.0, math.pi, 8.5], dtype=np.float32)
        self.observation_space = spaces.Box(-high, high, dtype=np.float32)
        rclpy.init(args=None)
        self.node = rclpy.create_node('cartpole_gym_env')
        self.cartpole_eff_pub = self.node.create_publisher(Float64MultiArray, "/effort_control/commands", 10)
        self.joint_state_sub = self.node.create_subscription(JointState, '/joint_states', self.joint_state_callback, 10 )
        self.current_observation = np.zeros(4, dtype=np.float32)
        self.state_received = False
        self.cartpole_reset_pub = self.node.create_publisher(Bool, "/cartpole/reset", 10)
        self.system_ready_sub = self.node.create_subscription(Bool, '/cartpole/ready', self.system_ready_cb, 10 )


        self.executor = rclpy.executors.SingleThreadedExecutor()
        self.executor.add_node(self.node)
        self.spin_thread = threading.Thread(target=self.executor.spin, daemon=True)
        self.spin_thread.start()
        self.system_ready = False

    def system_ready_cb(self, msg):
        self.system_ready = msg.data

    def joint_state_callback(self, msg):
        try:
     

            self.current_observation = np.array([
                msg.position[0],
                msg.velocity[0],
                bound_angle(msg.position[1]),
                msg.velocity[1]
            ], dtype=np.float32)
            
            self.state_received = True
        except ValueError:
            # Joint names not found
            pass
    
    def step(self, action):
        """
        ...
        """
        if not self.state_received:
            # If no state has been received yet, wait
            time.sleep(0.01)
            return self.current_observation, 0.0, False, False, {}
        
        eff_msg = Float64MultiArray()
        eff_msg.data = [float(action[0])]
        self.cartpole_eff_pub.publish(eff_msg)
        time.sleep(0.01)  
        obs = self.current_observation.copy()
        reward = 1.0  
                
        done = bool(
            obs[0] < -2 or obs[0] > 2 or
            obs[2] < -math.pi/4 or obs[2] > math.pi/4 or 
            math.fabs( obs[3] > 0.3 ) or 
            math.fabs( obs[1] > 1.0 )
        )

        if( math.fabs( obs[1] > 1.0 ) ): 
           reward = -10
        
        truncated = False  # You can set logic to handle truncation if necessary
        info = {}
        
        return obs, reward, done, truncated, info
    
    def reset(self, seed=None, options=None):
        if seed is not None:
             np.random.seed(seed)
            

        reset_data = Bool()
        reset_data.data = True
        self.cartpole_reset_pub.publish( reset_data )
        time.sleep(0.5)

        while( not self.system_ready ):
            time.sleep(0.001)

        info = {}
        return self.current_observation, info
    

    def close(self):
        """
        Clean up the environment.
        """
        self.executor.shutdown()
        self.node.destroy_node()
        rclpy.shutdown()


