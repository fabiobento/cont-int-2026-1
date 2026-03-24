# Define a versão mínima exigida do sistema de compilação CMake
cmake_minimum_required(VERSION 3.8)

# Define o nome do projeto (deve ser o mesmo nome contido no package.xml)
project(turtle_controller_cpp)

# Adiciona flags de compilação rigorosas caso o compilador seja GCC ou Clang.
# Isso ativa vários alertas (ex: variáveis não utilizadas) para melhorar a qualidade do código.
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Busca os pacotes do ROS 2 dos quais este projeto depende
# ament_cmake: Macros e funções principais de build do ROS 2
find_package(ament_cmake REQUIRED)
# rclcpp: Acesso às bibliotecas cliente C++ (como criar o nó, publishers, etc)
find_package(rclcpp REQUIRED)
# geometry_msgs: Acesso às classes de mensagens como o Twist
find_package(geometry_msgs REQUIRED)
# turtlesim: Acesso às interfaces específicas do simulador, como Pose
find_package(turtlesim REQUIRED)

# Declara a criação de um executável chamado "turtle_controller"
# Ele será compilado a partir do código-fonte localizado em "src/turtle_controller.cpp"
add_executable(turtle_controller src/turtle_controller.cpp)

# Vincula (link) as bibliotecas e diretórios de acesso (includes) dos pacotes ROS 2
# a este executável específico para que ele seja compilado corretamente
ament_target_dependencies(turtle_controller rclcpp geometry_msgs turtlesim)

# Instala o executável recém-criado na pasta de binários específicos de projeto
# Esta regra é o que permite o uso do comando `ros2 run turtle_controller_cpp turtle_controller`
install(TARGETS
 turtle_controller
 DESTINATION lib/${PROJECT_NAME}/
)

# Esta função finaliza as configurações do pacote, e cria ganchos (hooks) necessários
# para a correta instalação e exportação das bibliotecas/executáveis para outros pacotes
ament_package()
