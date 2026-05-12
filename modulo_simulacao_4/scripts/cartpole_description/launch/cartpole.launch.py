
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.substitutions import FindPackageShare
from launch.actions import ExecuteProcess, IncludeLaunchDescription

import time
def generate_launch_description():

    ld = LaunchDescription()
    xacro_path = 'urdf/cartpole.urdf.xacro'

    robot_description = PathJoinSubstitution([
        get_package_share_directory('cartpole_description'),	
        xacro_path
    ])

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description':Command(['xacro ', robot_description])
        }]
    )

    # Spawn
    spawn_node = Node(package='ros_gz_sim', executable='create',
                 arguments=[
                    '-name', 'cartpole',
                    '-x', '0',
                    '-y', '0',
                    '-z', '0',
                    '-r', '0',
                    '-p', '0',
                    '-Y', '0.0',
                    '-topic', '/robot_description'],
                 output='screen')

    
    ignition_gazebo_node = IncludeLaunchDescription( PythonLaunchDescriptionSource(
                [PathJoinSubstitution([FindPackageShare('ros_gz_sim'),
                                       'launch',
                                       'gz_sim.launch.py'])]),
                                        launch_arguments=[('gz_args', [' -r -v 4 empty.sdf'])])
   

    load_joint_state_broadcaster = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'joint_state_broadcaster'],
        output='screen'
    )

    
    load_stick_effort_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'stick_effort_control'],
        output='screen'
    )

    load_effort_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'effort_control'],
        output='screen'
    )

    ld.add_action( robot_state_publisher_node )
    ld.add_action( spawn_node )
    ld.add_action( ignition_gazebo_node )
    ld.add_action( load_joint_state_broadcaster )
    ld.add_action( load_stick_effort_controller )
    ld.add_action( load_effort_controller )

    return ld
