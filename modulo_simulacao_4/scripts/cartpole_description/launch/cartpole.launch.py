"""
Módulo de Inicialização (Launch File) do Cartpole no ROS 2.

Este script é responsável por configurar e iniciar todos os nós necessários para
a simulação do robô Cartpole no ambiente Gazebo (Ignition), além de carregar
seus controladores e publicar o estado do robô.
"""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration, Command
from launch_ros.substitutions import FindPackageShare

# IMPORTAÇÃO ADICIONADA: Necessária para forçar a leitura do XML como String pura
from launch_ros.parameter_descriptions import ParameterValue 

import time

def generate_launch_description():
    """
    Gera a descrição de inicialização (Launch Description) do sistema.
    
    Este método instancia e retorna um objeto LaunchDescription contendo as ações:
    - Inicialização do 'robot_state_publisher' para ler o arquivo Xacro/URDF.
    - Criação do ambiente de simulação do Gazebo.
    - Inserção (Spawn) do modelo tridimensional do Cartpole no mundo simulado.
    - Carregamento e ativação dos controladores (joint_state_broadcaster, 
      stick_effort_control e effort_control) através do ros2_control.

    Returns:
        LaunchDescription: Descrição completa com os nós e processos a serem executados.
    """

    ld = LaunchDescription()
    
    # Caminho relativo para o arquivo de descrição do robô
    xacro_path = 'urdf/cartpole.urdf.xacro'

    # Monta o caminho completo até o arquivo xacro
    robot_description = PathJoinSubstitution([
        get_package_share_directory('cartpole_description'),    
        xacro_path
    ])

    # Nó robot_state_publisher: converte o Xacro em URDF e publica as transformações de TF
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            # CORREÇÃO APLICADA: Envelopando o Command com ParameterValue(..., value_type=str)
            'robot_description': ParameterValue(Command(['xacro ', robot_description]), value_type=str)
        }]
    )

    # Nó de Spawn: responsável por instanciar (colocar) o modelo do robô dentro da simulação no Gazebo
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

    # Inicialização do simulador Ignition Gazebo com um mundo vazio
    ignition_gazebo_node = IncludeLaunchDescription( PythonLaunchDescriptionSource(
                [PathJoinSubstitution([FindPackageShare('ros_gz_sim'),
                                       'launch',
                                       'gz_sim.launch.py'])]),
                                        launch_arguments=[('gz_args', [' -r -v 4 empty.sdf'])])
   
    # Processo do ros2_control para carregar e ativar o publicador de estados das juntas
    load_joint_state_broadcaster = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'joint_state_broadcaster'],
        output='screen'
    )

    # Processo do ros2_control para carregar e ativar o controlador de esforço do pêndulo
    load_stick_effort_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'stick_effort_control'],
        output='screen'
    )

    # Processo do ros2_control para carregar e ativar o controlador de esforço do carrinho
    load_effort_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'effort_control'],
        output='screen'
    )

    # Adiciona todos os nós e processos na descrição de inicialização para execução
    ld.add_action( robot_state_publisher_node )
    ld.add_action( spawn_node )
    ld.add_action( ignition_gazebo_node )
    ld.add_action( load_joint_state_broadcaster )
    ld.add_action( load_stick_effort_controller )
    ld.add_action( load_effort_controller )

    return ld