# ROS 2 Cheat Sheet: A Patrulha Autônoma

### 🧘‍♂️ O "Mantra" do Desenvolvimento

Sempre que alterar o código, repita este ciclo:

1. **Compilar (Build):** `colcon build --packages-select <pacote> --symlink-install` 


2. **Ativar (Source):** `source ~/.bashrc` (ou `source install/setup.bash`) 


3. **Executar (Run):** `ros2 run <pacote> <executavel>` 


### 📦 Gestão de Workspace e Pacotes

| Comando | Descrição |
| --- | --- |
| `cd ~/master_ros2_ws` | Navega para a raiz do workspace.
|
| `ros2 pkg list \| grep my_` | Verifica se seus pacotes foram instalados corretamente.
|
| `colcon build --packages-select my_py_pkg` | Compila apenas o pacote Python (economiza tempo).
|



### 🐢 Simulação e Controle (Turtlesim)

*  **Abrir o Simulador:** `ros2 run turtlesim turtlesim_node` 


* **Controle Manual (Teclado):** `ros2 run turtlesim turtle_teleop_key` 


* **Resetar a Tartaruga:** `ros2 service call /reset std_srvs/srv/Empty {}` 


### 🔍 Inspeção do Sistema (Introspecção)

* **Listar Nós Ativos:** `ros2 node list` 


* **Ver "Raio-X" de um Nó:** `ros2 node info /patrulha_node` 


* **Ver Grafos de Comunicação:** `rqt` (selecionar *Node Graph*) 


* **Monitorar Dados do Tópico:** `ros2 topic echo /turtle1/cmd_vel` 



### 💡 Dicas de Sobrevivência no Terminal

* **Interromper qualquer nó:** `Ctrl + C`.


* **Renomear nó na execução:** `ros2 run my_py_pkg patrulha --ros-args -r __node:=novo_nome`.


* **Permissão de arquivo:** Se o `ros2 run` der erro de permissão, use `chmod +x nome_do_arquivo.py`.


* **Erro de 'Wget' no Docker:** `docker exec -u root ros2_dev apt update && apt install wget -y`.

