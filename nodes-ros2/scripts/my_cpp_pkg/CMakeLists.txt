# Define a versão mínima exigida do sistema de compilação CMake
cmake_minimum_required(VERSION 3.8)

# Define o nome do projeto (deve corresponder ao nome no package.xml)
project(my_cpp_pkg)

# Adiciona flags de compilação rigorosas caso o compilador seja GCC ou Clang.
# Isso ativa vários alertas (ex: variáveis não utilizadas) para manter e melhorar a qualidade do código.
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Busca as dependências (pacotes e bibliotecas adicionais do ROS 2) necessárias para compilar o código
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)

# Declara a criação de um executável chamado "test_node" 
# Ele será compilado a partir do código original "src/my_first_node.cpp"
add_executable(test_node src/my_first_node.cpp)

# Declara a criação de um executável chamado "supervisor" 
# Ele será compilado a partir do código do novo nó "src/supervisor_node.cpp"
add_executable(supervisor src/supervisor_node.cpp)

# Vincula (link) as bibliotecas e diretórios de acesso de "rclcpp" ao executável do nó de teste
ament_target_dependencies(test_node rclcpp)

# Vincula as dependências de "rclcpp" ao executável do nó supervisor
ament_target_dependencies(supervisor rclcpp)

# Instala os dois executáveis (test_node e supervisor) na pasta correta do pacote
# Esta etapa é obrigatória para que o ROS 2 consiga acessá-los através do comando "ros2 run my_cpp_pkg <executável>"
install(TARGETS
 test_node
 supervisor
 DESTINATION lib/${PROJECT_NAME}/
)

# Função final que aplica as configurações do ament_cmake e exporta o pacote compilado
ament_package()
