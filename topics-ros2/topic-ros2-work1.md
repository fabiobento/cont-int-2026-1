## Atividade Prática 3: Controle em Malha Fechada e Interfaces Personalizadas

### 1. Objetivo

Desenvolver um controlador de malha fechada que utiliza a posição real do robô (`/turtle1/pose`) para decidir as ações de controle, eliminando o erro acumulado do *Dead Reckoning*. Além disso, criaremos uma interface personalizada para monitorar o status do sistema.


### 2. Parte A: Criando a Interface Personalizada `RobotStatus`

Para monitorar o robô de forma mais profissional, não usaremos apenas textos genéricos. Vamos criar um pacote dedicado a interfaces.

1. **Criar o pacote de interfaces**:
Se você ainda não criou o pacote `my_robot_interfaces`, crie-o agora:

```bash
cd ~/master_ros2_ws/src
ros2 pkg create my_robot_interfaces

```


2. **Definir a mensagem**: Dentro da pasta `my_robot_interfaces`, crie a pasta `msg` e o arquivo `RobotStatus.msg` com o seguinte conteúdo:

```msg
float64 linear_velocity
float64 angular_velocity
string current_state
```

3. Adicione as configurações necessárias no `package.xml` e `CMakeLists.txt` do pacote `my_robot_interfaces` conforme visto na seção [Criando uma nova interface de tópico](https://github.com/fabiobento/cont-int-2026-1/blob/main/topics-ros2/topics-ros2.md#criando-uma-nova-interface-de-t%C3%B3pico) da [Aula 3: Tópicos – Enviando e Recebendo Mensagens entre Nós](https://github.com/fabiobento/cont-int-2026-1/blob/main/topics-ros2/topics-ros2.md) e compile o pacote.

### 3. Parte B: O Controlador de Malha Fechada (`turtle_closed_loop`)

Agora, vamos evoluir o nó da [Atividade Prática 2: Controle de Trajetória em Malha Aberta (Dead Reckoning)](https://github.com/fabiobento/cont-int-2026-1/blob/main/nodes-ros2/nodes-ros2-work2.md). Em vez de contar "ticks" de um Timer, o robô vai agir com base na posição lida do tópico `/turtle1/pose`.

**Instruções de Implementação:**

1. **Assinatura de Pose**: O nó deve assinar o tópico `/turtle1/pose` (interface `turtlesim/msg/Pose`).


2. **Lógica de Decisão**: No *callback* da pose, verifique a coordenada $X$.
* **Se $X < 5.5$**: Publique velocidade linear `1.0` e angular `1.0`.
* **Se $X \geq 5.5$**: Publique velocidade linear `2.0` e angular `2.0`.


3. **Publicação de Status**: Além do comando de movimento, o nó deve publicar no novo tópico `/robot_status` usando a interface que você criou na Parte A.


### 4. Parte C: Integração com o Supervisor (C++)

O nó **Supervisor** criado na Atividade Prática 1 deve ser mantido. Ele continuará monitorando o sistema, mas agora você deve verificar no `rqt_graph` como o fluxo de dados mudou: a tartaruga agora "fala" com o seu controlador, que por sua vez "fala" com os motores.

### 5. Validação e Inspeção

Após compilar seu workspace com `colcon build --symlink-install`, execute os testes:

1. **Terminal 1**: Inicie o simulador (`ros2 run turtlesim turtlesim_node`).


2. **Terminal 2**: Inicie seu novo controlador de malha fechada.
3. **Terminal 3**: Monitore as mensagens personalizadas:
```bash
ros2 topic echo /robot_status
```


4. **Terminal 4**: Use o "multímetro virtual" do ROS 2 para ver a pose real:
```bash
ros2 topic echo /turtle1/pose

```


---

### Desafio Final da Aula 3

Utilize o comando `ros2 bag record` para gravar 30 segundos da trajetória da sua tartaruga em malha fechada. Depois, feche o nó do controlador e use o `ros2 bag play` para ver se a tartaruga repete o movimento exatamente como gravado.

---
---
> **Atenção:**
>
>Pelo bem de seu aprendizado, tente realizar as etapas acima sem ler as informações adiante
---
---

## GABARITO

### Controlador em malha fechada em python

Para o caso de que você esteja com dificuldades, forneço abaixo o código-fonte base para o novo controlador de malha fechada em Python, integrando a leitura da pose real da tartaruga e a publicação do status personalizado.

#### Código: `turtle_closed_loop.py`

Este script deve ser salvo em `~/master_ros2_ws/src/my_py_pkg/my_py_pkg/`.

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
# Importando sua interface personalizada
from my_robot_interfaces.msg import RobotStatus 

class TurtleClosedLoopNode(Node):
    def __init__(self):
        super().__init__("turtle_closed_loop")
        
        # 1. Publicador para os motores da tartaruga
        self.cmd_vel_publisher_ = self.create_publisher(
            Twist, "/turtle1/cmd_vel", 10)
        
        # 2. Publicador para o status personalizado (Atividade Parte A)
        self.status_publisher_ = self.create_publisher(
            RobotStatus, "/robot_status", 10)
        
        # 3. Assinante para a Pose (Realimentação/Sensor)
        # O callback será acionado sempre que a tartaruga se mover
        self.pose_subscriber_ = self.create_subscription(
            Pose, "/turtle1/pose", self.callback_turtle_pose, 10)
        
        self.get_logger().info("Controlador de Malha Fechada com Status Personalizado Iniciado!")

    def callback_turtle_pose(self, msg: Pose):
        """
        Este é o coração do controlador. A ação de controle é calculada
        toda vez que uma nova posição (X, Y, theta) é recebida.
        """
        cmd = Twist()
        status = RobotStatus()

        
        if msg.x < 5.5:
            cmd.linear.x = 1.0
            cmd.angular.z = 1.0
            status.current_state = "Lado Esquerdo: Velocidade Normal" 
        else:
            cmd.linear.x = 2.0
            cmd.angular.z = 2.0
            status.current_state = "Lado Direito: Velocidade Rápida" 

        # Publica o comando de velocidade (Atuador)
        self.cmd_vel_publisher_.publish(cmd)

        # Preenche e publica o status personalizado
        status.linear_velocity = cmd.linear.x
        status.angular_velocity = cmd.angular.z
        self.status_publisher_.publish(status)

def main(args=None):
    rclpy.init(args=args)
    node = TurtleClosedLoopNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
```

* **Ponteiros de Memória e Objetos:** Observe que criamos os objetos `Twist()` e `RobotStatus()` dentro do *callback*. Isso garante que cada leitura de sensor gere uma resposta de controle fresca e independente.


* **Sem Timer:** Note a ausência do `self.create_timer`. Em sistemas de controle de alto desempenho, é comum sincronizar a malha de controle com a taxa de atualização do sensor (evento), e não com um relógio fixo.


* **Semântica:** O uso da string `current_state` na nossa interface personalizada permite que um supervisor humano ou outro nó entenda o que o controlador está "pensando".

>Além disso:
> 
> 1. Não esqueça de adicionar `<depend>turtlesim</depend>` e `<depend>my_robot_interfaces</depend>` no seu `package.xml`.
>
> 2. Torne o arquivo executável com `chmod +x`.
>
> 3. Compile o workspace na raiz com `colcon build --symlink-install`.

### Supervisor em C++

Para garantir que o seu nó **Supervisor em C++** monitore corretamente o sistema utilizando a interface personalizada, aqui está o código-fonte sugerido.

Este script deve ser salvo em `~/master_ros2_ws/src/my_cpp_pkg/src/supervisor_node.cpp`.

### Código: `supervisor_node.cpp`

```cpp
#include "rclcpp/rclcpp.hpp"
#include "turtlesim/msg/pose.hpp"
#include "my_robot_interfaces/msg/robot_status.hpp"

using std::placeholders::_1;

class SupervisorNode : public rclcpp::Node {
public:
    SupervisorNode() : Node("supervisor_node") {
        // 1. Assinante para o Status Personalizado (Criado na Atividade 3)
        status_subscriber_ = this->create_subscription<my_robot_interfaces::msg::RobotStatus>(
            "/robot_status", 10, std::bind(&SupervisorNode::callback_status, this, _1));

        // 2. Assinante para a Pose (Para monitorar a posição real)
        pose_subscriber_ = this->create_subscription<turtlesim::msg::Pose>(
            "/turtle1/pose", 10, std::bind(&SupervisorNode::callback_pose, this, _1));

        RCLCPP_INFO(this->get_logger(), "Supervisor de Segurança e Status Iniciado.");
    }

private:
    void callback_status(const my_robot_interfaces::msg::RobotStatus::SharedPtr msg) {
        // Exibe o status que o controlador está reportando
        RCLCPP_INFO(this->get_logger(), "[STATUS] Estado: %s | Vel Lin: %.2f", 
                    msg->current_state.c_str(), msg->linear_velocity);
    }

    void callback_pose(const turtlesim::msg::Pose::SharedPtr msg) {
        // Monitoramento de segurança: Alerta se a tartaruga chegar perto das bordas
        if (msg->x > 9.0 || msg->x < 2.0 || msg->y > 9.0 || msg->y < 2.0) {
            RCLCPP_WARN(this->get_logger(), "[ALERTA] Tartaruga próxima à parede! Posição: (%.2f, %.2f)", 
                        msg->x, msg->y);
        }
    }

    rclcpp::Subscription<my_robot_interfaces::msg::RobotStatus>::SharedPtr status_subscriber_;
    rclcpp::Subscription<turtlesim::msg::Pose>::SharedPtr pose_subscriber_;
};

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<SupervisorNode>());
    rclcpp::shutdown();
    return 0;
}

```

* **Interfaces Customizadas:** Para incluir sua mensagem em C++, o padrão é `<nome_do_pacote>/msg/<nome_do_arquivo_em_snake_case>.hpp`. Por isso usamos `my_robot_interfaces/msg/robot_status.hpp`.


* **Ponteiros Compartilhados:** Em C++, as mensagens recebidas via callback são sempre `SharedPtr` (ponteiros inteligentes). Lembre-se de usar a seta (`->`) para acessar os campos, como em `msg->current_state`.

> Além disso:
> 
> *Certifique-se de que o bloco de dependências do supervisor inclua todos os pacotes utilizados no código acima:
> 
> ```cmake
> add_executable(supervisor src/supervisor_node.cpp)
> ament_target_dependencies(supervisor rclcpp turtlesim > my_robot_interfaces)
> 
> ```
