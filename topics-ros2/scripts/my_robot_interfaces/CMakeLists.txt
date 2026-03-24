# Define a versão mínima exigida do sistema de compilação CMake
cmake_minimum_required(VERSION 3.8)

# Define o nome do projeto (deve ser o mesmo nome contido no package.xml)
project(my_robot_interfaces)

# Adiciona flags de compilação rigorosas caso o compilador seja GCC ou Clang.
# Isso ativa vários alertas para manter e melhorar a qualidade do código.
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Busca os pacotes do ROS 2 dos quais este projeto depende
# ament_cmake: Essencial para construir e gerografar pacotes no padrão do ROS 2
find_package(ament_cmake REQUIRED)
# rosidl_default_generators: Pacote contendo as ferramentas para ler arquivos .msg/.srv/.action
# e gerar os respectivos códigos-fonte (em C++, Python, etc.) para sua utilização
find_package(rosidl_default_generators REQUIRED)

# Solicita ao sistema que processe as interfaces (mensagens) listadas e gere seus códigos
# É fundamental que o caminho inclua a pasta "msg/" antes do nome do arquivo
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/HardwareStatus.msg"
)

# Exporta as dependências necessárias para a infraestrutura de mensagens funcionar em tempo de execução
# Isso garante que quem importar suas mensagens de `my_robot_interfaces` terá acesso às dependências subjacentes
ament_export_dependencies(rosidl_default_runtime)

# Macro final obrigatória que processa todos os passos definidos e gera arquivos para os demais pacotes encontrarem este
ament_package()
