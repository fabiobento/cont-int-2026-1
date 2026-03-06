#!/bin/bash
# Script de automação para o Laboratório de Controle Inteligente

WORKSPACE_DIR=~/master_ros2_ws
PKG_NAME="controle_pkg"
NODE_NAME="controle_aberto_node"

echo "=================================================="
echo " Iniciando a configuração do Laboratório..."
echo "=================================================="

# 1. Navega para o diretório de código-fonte do workspace
mkdir -p $WORKSPACE_DIR/src
cd $WORKSPACE_DIR/src || exit

# 2. Cria o pacote ROS 2 em Python com as dependências necessárias
echo "-> Criando o pacote '$PKG_NAME'..."
ros2 pkg create $PKG_NAME --build-type ament_python --dependencies rclpy geometry_msgs > /dev/null 2>&1

# 3. Cria o arquivo do nó Python com o código da FSM (Máquina de Estados)
echo "-> Gerando o código-fonte do nó..."
cat << 'EOF' > $PKG_NAME/$PKG_NAME/$NODE_NAME.py
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class ControleAbertoNode(Node):
    def __init__(self):
        super().__init__("controle_aberto")
        
        # Parâmetros de Tempo Discreto
        self.Ts_ = 0.5  
        self.k_ = 0     
        
        self.pub_motor = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.timer_ = self.create_timer(self.Ts_, self.loop_controle)
        self.estado_ = 0 
        
        self.get_logger().info("Controlador de Malha Aberta Iniciado!")

    def loop_controle(self):
        msg = Twist()
        
        # ESTADO 0: Andar (N = 4 ticks)
        if self.estado_ == 0:
            msg.linear.x = 1.0
            msg.angular.z = 0.0
            self.k_ += 1
            self.get_logger().info(f"Andando... Tick {self.k_}/4")
            
            if self.k_ >= 4:
                self.estado_ = 1  
                self.k_ = 0       
                
        # ESTADO 1: Girar (N = 2 ticks)
        elif self.estado_ == 1:
            msg.linear.x = 0.0
            msg.angular.z = 1.57 
            self.k_ += 1
            self.get_logger().info(f"Girando... Tick {self.k_}/2")
            
            if self.k_ >= 2:
                self.estado_ = 0  
                self.k_ = 0
                
        self.pub_motor.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = ControleAbertoNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
EOF

# 4. Dá permissão de execução ao script Python
chmod +x $PKG_NAME/$PKG_NAME/$NODE_NAME.py

# 5. Adiciona o executável no setup.py de forma automática
echo "-> Configurando o entry_point no setup.py..."
sed -i "s/'console_scripts': \[/'console_scripts': [\n            'controle_aberto = $PKG_NAME.$NODE_NAME:main',/" $PKG_NAME/setup.py

echo "=================================================="
echo "✅ Pacote configurado com sucesso na pasta src!"
echo ""
echo " Próximos passos para executar:"
echo " 1. cd $WORKSPACE_DIR"
echo " 2. colcon build --packages-select $PKG_NAME --symlink-install"
echo " 3. source ~/.bashrc"
echo " 4. ros2 run turtlesim turtlesim_node (Abra um novo terminal)"
echo " 5. ros2 run $PKG_NAME controle_aberto (No terminal atual)"
echo "=================================================="