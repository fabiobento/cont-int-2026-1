# Define a versão mínima exigida do sistema de compilação CMake
cmake_minimum_required(VERSION 3.8)

# Define o nome do projeto (deve corresponder ao declarado no package.xml)
project(my_cpp_pkg)

# Adiciona flags de compilação rigorosas caso o compilador seja GCC ou Clang.
# Isso ativa vários alertas para ajudar a manter a qualidade do código C++.
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Busca os pacotes do ROS 2 dos quais este projeto depende para compilar
find_package(ament_cmake REQUIRED)         # Macros essenciais de build do ROS 2
find_package(rclcpp REQUIRED)              # Biblioteca principal do ROS 2 para C++
find_package(example_interfaces REQUIRED)  # Pacote que contém mensagens padronizadas e tipos de dados de exemplo

# ==============================================================================
# Declaração e Vínculo dos Executáveis (Nós)
# ==============================================================================

# 1. Nó de teste básico
add_executable(test_node src/my_first_node.cpp)
ament_target_dependencies(test_node rclcpp)

# 2. Nó Publicador de números
add_executable(number_publisher src/number_publisher.cpp)
# Note que ele precisa compilar junto com example_interfaces, pois utiliza as mensagens dele
ament_target_dependencies(number_publisher rclcpp example_interfaces)

# 3. Nó Contador de números
add_executable(number_counter src/number_counter.cpp)
# Da mesma forma, depende do example_interfaces para ler as mensagens recebidas
ament_target_dependencies(number_counter rclcpp example_interfaces)

# ==============================================================================
# Regras de Instalação e Finalização
# ==============================================================================

# Instala todos os 3 executáveis criados na pasta destino adequada (lib/my_cpp_pkg)
# É esta diretiva que torna possível executar "ros2 run my_cpp_pkg <nome_do_nó>"
install(TARGETS
 test_node
 number_publisher
 number_counter
 DESTINATION lib/${PROJECT_NAME}/
)

# Macro final obrigatória que processa todos os passos anteriores e integra o pacote
# no ambiente (workspace) do ROS 2
ament_package()
