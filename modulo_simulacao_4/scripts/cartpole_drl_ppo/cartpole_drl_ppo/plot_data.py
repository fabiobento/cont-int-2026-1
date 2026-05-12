#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import matplotlib.pyplot as plt
import time
import os
import math

def bound_angle(angle):
    # Normalize the angle between -pi and pi
    bounded_angle = (angle + math.pi) % (2 * math.pi) - math.pi
    return bounded_angle


class JointStateRecorder(Node):
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
        # Append the positions and timestamps
        self.joint_positions.append(msg.position)
        self.timestamps.append(self.get_clock().now().seconds_nanoseconds()[0])
        self.get_logger().info(f"Recording joint positions: {msg.position}")

        self.joint_velocity.append(msg.velocity)
        self.timestamps_vel.append(self.get_clock().now().seconds_nanoseconds()[0])


    def save_data(self):
        # Save the collected joint positions to a file
        data_dir = os.path.join(os.getcwd(), 'joint_states_data')
        os.makedirs(data_dir, exist_ok=True)
        file_path = os.path.join(data_dir, f'joint_positions_{int(time.time())}.txt')
        
        with open(file_path, 'w') as file:
            for t, positions in zip(self.timestamps, self.joint_positions):
                file.write(f"{t}, {', '.join(map(str, positions))}\n")
        
        self.get_logger().info(f"Joint position data saved to {file_path}")
        return file_path

    def plot_data(self):
        # Assuming we're interested in the first joint's position for simplicity
        joint_positions_array = [pos[0] for pos in self.joint_positions]  # Adjust index for other joints
        plt.figure()
        plt.plot(self.timestamps, joint_positions_array)
        plt.title('Cart position')
        plt.xlabel('Time (s)')
        plt.ylabel('Position (m)')
        plt.grid(True)
        #plt.show()

        joint_positions_array = [pos[1] for pos in self.joint_positions]  # Adjust index for other joints
        plt.figure()
        plt.plot(self.timestamps, joint_positions_array)
        plt.title('Pole orientation')
        plt.xlabel('Time (s)')
        plt.ylabel('Position (rad)')
        plt.grid(True)
        
        joint_velocity_array = [vel[0] for vel in self.joint_velocity]  # Adjust index for other joints
        plt.figure()
        plt.plot(self.timestamps_vel, joint_velocity_array)
        plt.title('Cart velocity')
        plt.xlabel('Time (s)')
        plt.ylabel('Velocity (m/s)')
        plt.grid(True)
        

        joint_velocity_array = [vel[1] for vel in self.joint_velocity]  # Adjust index for other joints
        plt.figure()
        plt.plot(self.timestamps_vel, joint_velocity_array)
        plt.title('Pole velocity')
        plt.xlabel('Time (s)')
        plt.ylabel('Rotation velocity (rad/s)')
        plt.grid(True)
        plt.show()
        '''

        '''
def main(args=None):
    rclpy.init(args=args)
    joint_state_recorder = JointStateRecorder()

    try:
        # Spin until manually interrupted
        rclpy.spin(joint_state_recorder)
    except KeyboardInterrupt:
        joint_state_recorder.get_logger().info('Saving and plotting data...')
        #joint_state_recorder.save_data()
        joint_state_recorder.plot_data()
    finally:
        joint_state_recorder.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
