"""
Módulo ROS 2 responsável por redefinir e estabilizar o sistema do Cartpole.

Este script implementa um nó que monitora o estado das juntas e, ao receber um comando 
de reset, utiliza controladores Proporcionais-Derivativos (PD) independentes para 
retornar o carrinho à posição inicial e estabilizar o pêndulo na posição vertical.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray, Bool
from sensor_msgs.msg import JointState
from threading import Thread
import math

# Função para garantir que o ângulo do pêndulo fique restrito entre -pi e pi
def bound_angle(angle):
    """
    Mantém o valor do ângulo delimitado no intervalo de -pi a pi radianos.

    Args:
        angle (float): Ângulo contínuo em radianos.

    Returns:
        float: O ângulo equivalente ajustado para o intervalo [-pi, pi].
    """
    bounded_angle = (angle + math.pi) % (2 * math.pi) - math.pi
    return bounded_angle

class CartPoleReset(Node):
    """
    Classe do nó ROS 2 responsável por executar o processo de reset do Cartpole.
    """
    def __init__(self):
        """
        Inicializa o nó, configurando as inscrições (subscriptions), publicadores
        (publishers) e o timer necessários para o controle das juntas do robô.
        """
        # Inicializa o nó (nomeado como 'yolo_node', embora controle o reset do cartpole)
        super().__init__('yolo_node')
        
        # Inscreve-se no tópico de estados das juntas para receber posições e velocidades
        self.js_sub = self.create_subscription(JointState, "/joint_states", self.js_cb, 10)
        
        # Publicadores de comandos de esforço (effort/torque) para o carrinho e para o pêndulo
        self.cartpole_eff_pub = self.create_publisher(Float64MultiArray, "/effort_control/commands", 10)
        self.system_ready_pub = self.create_publisher(Bool, "/cartpole/ready", 10)
        self.cartpole__reset_sub = self.create_subscription(Bool, "/cartpole/reset", self.reset, 10)
        self.stick_eff_pub = self.create_publisher(Float64MultiArray, "/stick_effort_control/commands", 10)
        
        # Publicador que indica se o sistema está pronto e inscrição para iniciar o reset
        self.system_ready_pub = self.create_publisher(Bool, "/cartpole/ready", 10)
        self.cartpole__reset_sub = self.create_subscription(Bool, "/cartpole/reset", self.reset_callback, 10)
        
        # Timer para publicar repetidamente que o sistema está pronto
        self.timer = self.create_timer(0.1, self.publish_system_ready)
        
        # Flags e variáveis de controle interno
        self.reset = False
        self.js_ready = False
        self.js = None
        self.system_ready = Bool()
        self.system_ready.data = True
    
    def main_loop(self): 
        """
        Loop de execução principal executado em uma thread separada.
        
        Este método aguarda um comando de reset e, em seguida, executa um 
        loop de controle a 100 Hz utilizando controladores PD para estabilizar 
        tanto a posição linear do carrinho quanto a posição angular do pêndulo.
        """
       
        rate = self.create_rate(2)
        
        # Aguarda até receber o primeiro dado de estado das juntas
        while not self.js_ready:
            rate.sleep()   
            
        # Loop principal enquanto o ROS estiver rodando
        while rclpy.ok():

            # Verifica se uma solicitação de reset foi recebida
            if( self.reset == True):
                # Publica que o sistema não está pronto durante o procedimento de reset
                self.system_ready.data = False
                self.system_ready_pub.publish(self.system_ready)
              
                # Taxa de controle interno de 100 Hz
                rate2 = self.create_rate(100)
                
                # Reseta a flag para evitar múltiplos resets simultâneos
                self.reset = False
         
                # Mensagens de comando
                cmd = Float64MultiArray()  
                stick_tau_cmd = Float64MultiArray()                
              
                # Ganhos PD para o controle do carrinho (linear)
                k = 0.8
                k2 = 0.2
                
                # Ganhos PD para o controle do pêndulo (angular)
                k_stick = 0.1
                k2_stick = 0.05
                
                # Variáveis de erro do pêndulo
                stick_e = 0.0
                prev_stick_e = 0.0
                stick_derivative = 0.0
                
                # Variáveis de erro do carrinho
                cart_e = 0 
                prev_cart_e = 0
                cart_e_derivative = 0
                
                # Obtendo posições iniciais
                cart_e = self.js.position[0]
                prev_cart_e = 0
                
                stick_js = bound_angle(self.js.position[1])
                
                # Enquanto o pêndulo estiver inclinado ou a velocidade do carrinho não for zero
                while ( (math.fabs( stick_js) > 0.05) or (math.fabs(self.js.velocity[0]) > 0.01) ) :
                     
                    # Controle PD do carrinho (aproximando da posição 0)
                    cart_e = (self.js.position[0])
                    cart_e_derivative = (cart_e - prev_cart_e) / (1.0/100.0)
                    cart_c = k*cart_e + k2*cart_e_derivative
                    cmd.data = [-cart_c]

                    # Controle PD do pêndulo (aproximando do ângulo 0)
                    stick_js = bound_angle(self.js.position[1])
                    
                    stick_e = math.fabs( stick_js )
                    stick_derivative = (stick_e - prev_stick_e) / (1.0/100.0)

                    tau = k_stick*stick_e + k2_stick*stick_derivative

                    # Ajusta a direção do torque dependendo de qual lado o pêndulo caiu
                    if ( stick_js > 0 ):
                        tau = -tau
                    
                    stick_tau_cmd.data = [tau]
                    
                    # Publica os torques / forças calculadas
                    self.cartpole_eff_pub.publish(cmd)
                    self.stick_eff_pub.publish(stick_tau_cmd)
                    
                    # Atualiza os estados anteriores
                    prev_stick_e = stick_e
                    prev_cart_e = cart_e

                    # Dorme para manter a frequência de 100 Hz
                    rate2.sleep()

                # Procedimento finalizado: o sistema está pronto novamente
                self.system_ready.data = True

            # Dorme no loop principal
            rate.sleep()

    def reset_callback(self, msg):
        """
        Callback acionado ao receber uma mensagem no tópico de reset.

    def reset(self, msg):
        self.reset = True

    # Função para publicar periodicamente que o sistema está pronto (ready)
    def publish_system_ready(self):
        """
        Publica repetidamente o status atual do sistema no tópico respectivo.
        """
        self.system_ready_pub.publish(self.system_ready)

    # Callback para atualizar os dados mais recentes das juntas
    def js_cb(self, msg):
        """
        Callback que atualiza a variável local de estados das juntas.

        Args:
            msg (sensor_msgs.msg.JointState): Mensagem contendo o estado atual das juntas.
        """
        self.js = msg
        self.js_ready = True

    # Inicia a thread separada para o loop de controle e permite que o nó receba mensagens
    def run( self ):
        """
        Inicia a execução do nó. 
        
        Cria uma thread paralela para executar o 'main_loop', garantindo que
        o spin do ROS 2 não seja bloqueado e as mensagens continuem sendo processadas.
        """
        main_loop_thread = Thread(target = self.main_loop, args = ())
        main_loop_thread.start()
        rclpy.spin(self)

def main(args=None):
    """
    Função principal de entrada do script. Inicializa a comunicação ROS 2 
    e coloca o nó em execução.
    """
    rclpy.init(args=args)

    node = CartPoleReset()
    node.run()

if __name__ == '__main__':
    main()
