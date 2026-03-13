# Trabalho Prático: A Patrulha Autônoma

## 1. Objetivo

Desenvolver um sistema com dois nós operando simultaneamente: um nó **Python** que controla o movimento da tartaruga e um nó **C++** que atua como supervisor de segurança. Você aplicará os conceitos de criação de pacotes, escrita de nós com POO e uso de Timers.

## 2. Preparação do Ambiente

1. Em um terminal dentro do container, inicie o simulador: `ros2 run turtlesim turtlesim_node`.


3. Certifique-se de que seu workspace `master_ros2_ws` está configurado e ativo no seu `.bashrc`.


---

## 3. Parte A: O Nó Python "Patrulheiro"

Navegue até o diretório de scripts do seu pacote Python: `cd ~/master_ros2_ws/src/my_py_pkg/my_py_pkg/`. Crie o arquivo `patrulha_node.py` com o código abaixo:

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist # Interface para comandos de velocidade 

class PatrulhaNode(Node):
    def __init__(self):
        super().__init__("patrulha_node") # Nome que aparecerá no 'ros2 node list' 
        self.publisher_ = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.timer_ = self.create_timer(2.0, self.executar_ronda) # Loop de controle temporal 
        self.fase_ = 0
        self.get_logger().info("Iniciando a ronda da tartaruga IFES...")

    def executar_ronda(self):
        msg = Twist()
        if self.fase_ % 2 == 0:
            msg.linear.x = 2.0 # Avança 
            self.get_logger().info("Status: Avançando!")
        else:
            msg.angular.z = 1.57 # Vira 90 graus 
            self.get_logger().info("Status: Virando a esquina...")
        self.publisher_.publish(msg)
        self.fase_ += 1

def main(args=None):
    rclpy.init(args=args)
    node = PatrulhaNode()
    rclpy.spin(node) # Mantém o robô "escutando" e o timer ativo 
    rclpy.shutdown()

if __name__ == "__main__":
    main()
```

---

## 4. Parte B: O Nó C++ "Supervisor" (Missão Extra)

Para garantir que a ronda está ocorrendo, crie um supervisor em C++. No diretório `~/master_ros2_ws/src/my_cpp_pkg/src/`, crie o arquivo `supervisor_node.cpp`:

```cpp
#include "rclcpp/rclcpp.hpp"

class SupervisorNode : public rclcpp::Node {
public:
    SupervisorNode() : Node("supervisor_node") {
        // Timer de 5 segundos para supervisão
        timer_ = this->create_wall_timer(
            std::chrono::seconds(5), std::bind(&SupervisorNode::check_status, this));
    }
private:
    void check_status() {
        RCLCPP_WARN(this->get_logger(), "[SUPERVISOR] Ronda em andamento. Sistema íntegro.");
    }
    rclcpp::TimerBase::SharedPtr timer_; // Ponteiro inteligente para o timer 
};

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<SupervisorNode>());
    rclcpp::shutdown();
    return 0;
}

```

---

## 5. Ciclo de Implementação e Validação

1.**Permissões:** Torne o arquivo Python executável: `chmod +x patrulha_node.py`.


2.**Configuração Python:** No `setup.py`, adicione em `console_scripts`: `'patrulha = my_py_pkg.patrulha_node:main',`.


3.**Configuração C++:** No `CMakeLists.txt`, adicione `add_executable(supervisor src/supervisor_node.cpp)` e as linhas de `ament_target_dependencies(supervisor rclcpp)` e `supervisor` em `install`.


4. **Build:** Na raiz do workspace: `cd ~/master_ros2_ws/` e`colcon build --symlink-install`.


5. **Execução Multi-Terminal:**
* Terminal 1: `ros2 run turtlesim turtlesim_node` 


* Terminal 2: `ros2 run my_py_pkg patrulha` 


* Terminal 3: `ros2 run my_cpp_pkg supervisor` 





### **Desafio Final**

Abra o `rqt_graph`. Você deverá ver o `patrulha_node` conectado à tartaruga, enquanto o `supervisor_node` opera de forma independente, provando a natureza multi-processo do ROS 2.

---
---
> **Atenção:**
>
>Pelo bem de seu aprendizado, tente realizar as etapas acima sem ler as informações adiante
---
---
## Arquivos de configuração

Aqui estão os arquivos de configuração completos e corrigidos. Eles seguem as regras de "ouro" discutidas na **Aula 2**: a localização correta do código, a declaração de dependências e a ordem das instruções.

### 1. Configuração do Pacote Python (`my_py_pkg`)

O arquivo `setup.py` deve conter o `entry_point` que mapeia o comando `patrulha` para a função `main` do seu script.

#### **setup.py**

```python
from setuptools import find_packages, setup

package_name = 'my_py_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Fabio Bento',
    maintainer_email='fbento@ifes.edu.br',
    description='Trabalho pratico de Patrulha ROS 2 no IFES',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "test_node = my_py_pkg.my_first_node:main",
            "patrulha = my_py_pkg.patrulha_node:main" # Novo executavel 
        ],
    },
)

```

### 2. Configuração do Pacote C++ (`my_cpp_pkg`)

No C++, o `CMakeLists.txt` precisa compilar o código fonte em um binário e instalá-lo na pasta correta para que o `ros2 run` o localize. Lembre-se: a linha `ament_package()` deve ser a última.

#### **CMakeLists.txt**

```cmake
cmake_minimum_required(VERSION 3.8)
project(my_cpp_pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Encontrar dependencias 
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)

# --- Executavel: test_node ---
add_executable(test_node src/my_first_node.cpp)
ament_target_dependencies(test_node rclcpp)

# --- Executavel: supervisor ---
add_executable(supervisor src/supervisor_node.cpp)
ament_target_dependencies(supervisor rclcpp)

# Instalacao dos executaveis 
install(TARGETS
  test_node
  supervisor
  DESTINATION lib/${PROJECT_NAME}/
)

ament_package() # Sempre a ultima linha 

```

### Dicas Técnicas:

* **Dependências:** O `geometry_msgs` foi adicionado no C++ para que, no futuro, vocês possam fazer o supervisor também ler as mensagens de velocidade, embora para este exercício básico de `RCLCPP_INFO` apenas o `rclcpp` baste.


* **O Erro Comum:** Se o `colcon build` falhar no Python, verifiquem a **vírgula** entre as linhas dos `console_scripts`. No C++, o erro comum é esquecer de listar o executável no bloco `install`.


* **Limpeza:** Se o ambiente ficar instável após muitas alterações, apaguem as pastas `build`, `install` e `log` e compile do zero.
