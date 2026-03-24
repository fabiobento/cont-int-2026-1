## Atividade Prática 2: Controle de Trajetória em Malha Aberta (Dead Reckoning)

### **Objetivo**

Aplicar conceitos de cinemática e tempo discreto ($T_s$) para fazer o `turtlesim` desenhar um quadrado perfeito. Você deve calcular quantos "ticks" do Timer são necessários para transladar e rotacionar, utilizando apenas lógica de tempo real em malha aberta.

### **O Conceito Teórico (Controle Discreto)**

Se o robô precisa andar uma distância $\Delta s$ com uma velocidade constante $v$, o tempo necessário é $t = \Delta s / v$.
No mundo digital do ROS 2, o tempo é medido em instantes discretos $k$ a cada disparo do Timer ($T_s$). O número de disparos necessários ($N$) para completar o movimento é:


$$N = \frac{\Delta s}{v \cdot T_s}$$

Você precisará programar uma Máquina de Estados Finita (FSM) simples que conta os instantes $k$ para alternar entre "Andar Reto" e "Girar 90 graus", sem nenhum feedback de sensor.

---

### **Roteiro da Atividade**

#### **1. O "Driver" Fornecido (Caixa Preta)**

Para que o robô se mova antes da Aula 3, incluam estas duas linhas no `__init__` do seu nó. Elas são o "cabo de energia" do motor:

```python
from geometry_msgs.msg import Twist
# ... dentro do __init__:
self.pub_motor = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

```

#### **2. O Desafio de Programação (Python)**

Crie o nó `controle_aberto_node.py`. Configure o Timer (`self.Ts_ = 0.5`) e implemente a lógica geométrica.

**Código:**

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class ControleAbertoNode(Node):
    def __init__(self):
        super().__init__("controle_aberto")
        
        # Parâmetros de Tempo Discreto
        self.Ts_ = 0.5  # Tempo de Amostragem (Segundos)
        self.k_ = 0     # Instante atual (tick)
        
        # Caixa Preta (Atuador)
        self.pub_motor = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        
        # O Timer é o "Clock" do nosso controlador
        self.timer_ = self.create_timer(self.Ts_, self.loop_controle)
        
        # Controle de Estado (0 = Andando, 1 = Girando)
        self.estado_ = 0 
        
        self.get_logger().info("Controlador de Malha Aberta Iniciado!")

    def loop_controle(self):
        msg = Twist()
        
        # ESTADO 0: Andar para frente por 2 metros (v = 1.0 m/s)
        # N = 2.0 / (1.0 * 0.5) = 4 ticks
        if self.estado_ == 0:
            msg.linear.x = 1.0
            msg.angular.z = 0.0
            self.k_ += 1
            self.get_logger().info(f"Andando... Tick {self.k_}/4")
            
            if self.k_ >= 4:
                self.estado_ = 1  # Muda para rotação
                self.k_ = 0       # Zera o contador k
                
        # ESTADO 1: Girar 90 graus (aprox. 1.57 rad) com w = 1.57 rad/s
        # N = 1.57 / (1.57 * 0.5) = 2 ticks
        elif self.estado_ == 1:
            msg.linear.x = 0.0
            msg.angular.z = 1.57 
            self.k_ += 1
            self.get_logger().info(f"Girando... Tick {self.k_}/2")
            
            if self.k_ >= 2:
                self.estado_ = 0  # Volta a andar
                self.k_ = 0
                
        # Aplica o esforço de controle na planta
        self.pub_motor.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = ControleAbertoNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()

```

#### **3. Ciclo ROS 2 (Prática da Aula 2)**

Lembre-se de:

1. Dar permissão: `chmod +x controle_aberto_node.py`.
2. Registrar nos `entry_points` do `setup.py` o seguinte: `"controle_aberto = my_py_pkg.controle_aberto_node:main"`.
3. Compilar na raiz do workspace (`cd ~/master_ros2_ws`): `colcon build --symlink-install`
4. Fazer o carregamento: source ~/.bashrc`
5. Rodar o simulador em um terminal(`ros2 run turtlesim turtlesim_node`) e o nó de controle(`ros2 run my_py_pkg controle_aberto`).

---

> **Observação**
> 
> Quando o robô terminar de desenhar alguns quadrados, observe a tela do simulador de perto.
> * "O quadrado está fechando perfeitamente no mesmo ponto inicial após várias voltas?"
>
>    * A resposta é não! O erro de integração numérica (_dead reckoning_) vai se acumulando.
>    * Como a malha é aberta, o controlador "acha" que virou exatamente 90 graus, mas a física do simulador (e do mundo real) tem pequenos atrasos.
>
> É por isso que na Aula 3 aprenderemos a ler o Tópico `/turtle1/pose`. Vamos fechar a malha e usar o erro real para corrigir a trajetória!"*.


# O Desafio do Triângulo

## 1. O Desafio

Você configurou um controlador digital que faz a tartaruga desenhar um **quadrado**. A sua tarefa agora é aplicar os conceitos de cinemática e controle em tempo discreto para alterar o código-fonte e fazer o robô desenhar um **triângulo equilátero**.

## 2. A Teoria (Equacionamento)

Em um triângulo equilátero, os ângulos internos são de $60^\circ$. No entanto, para que o robô faça a curva correta, ele deve rotacionar o **ângulo externo**, que é de $120^\circ$.

Convertendo para radianos:


$$120^\circ = \frac{2\pi}{3} \approx 2.094 \text{ rad}$$

Sabendo que o nosso controlador opera com um Tempo de Amostragem ($T_s$) de $0.5$ segundos, você precisa calcular a velocidade angular ($w$) e o número de instantes (ticks $N$) necessários para completar a curva.

**Exemplo de dimensionamento:**
Se definirmos $N = 4$ ticks (ou seja, a curva vai durar $2.0$ segundos no total), a velocidade angular enviada ao motor deve ser:


$$w = \frac{2.094}{4 \cdot 0.5} = 1.047 \text{ rad/s}$$

## 3. Alterando a Malha de Controle

Abra o arquivo gerado pelo script no seu VS Code:
`~/master_ros2_ws/src/controle_pkg/controle_pkg/controle_aberto_node.py`

Localize a função `loop_controle(self)` e altere a lógica do **ESTADO 1** (fase de rotação) para refletir os cálculos do triângulo:

```python
        # ESTADO 1: Girar 120 graus (aprox. 2.094 rad)
        # Escolhemos N = 4 ticks. Então w = 1.047 rad/s
        elif self.estado_ == 1:
            msg.linear.x = 0.0
            msg.angular.z = 1.047  # Nova velocidade angular
            self.k_ += 1
            self.get_logger().info(f"Girando 120 graus... Tick {self.k_}/4")
            
            if self.k_ >= 4: # Novo limite de ticks
                self.estado_ = 0  # Volta a andar
                self.k_ = 0

```

*Dica: Lembre-se de sempre rodar o `colcon build --packages-select my_py_pkg --symlink-install` na raiz do workspace após salvar o arquivo!*

