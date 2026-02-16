
# PLANO DE ENSINO: CONTROLE INTELIGENTE (2026/1) - Ênfase em ROS 2

- **Disciplina:** Controle Inteligente (20261.ENEL.8)
- **Ferramentas Principais:** Python 3, PyTorch, ROS 2 (Distro Jazzy/Humble), Gazebo Sim.


## Introdução
A disciplina de Controle Inteligente é uma oportunidade para os alunos se aprofundarem na interseção entre Inteligência Artificial e diversas áreas da Engenharia Elétrica.

Nesse semestre aplicaremos os conceitos de Inteligência Artificial em um caso de uso de Robótica. Portanto, o [**ROS 2 (Robot Operating System)**](https://www.ros.org/) será uma ferramenta central ao lado de [**Python**](https://www.python.org/) e [**PyTorch**](https://pytorch.org/), a fim de que a disciplina tenha uma forte dimensão profissionalizante. O ROS 2 é o padrão industrial para robótica e fornece a infraestrutura ("middleware") necessária para conectar os algoritmos de Inteligência Artificial (PyTorch) aos sensores e atuadores do robô (simulado ou real).

## 1. EMENTA
Fundamentos de Inteligência Computacional. Arquitetura de Software para Robótica (ROS 2). Redes Neurais Artificiais e Deep Learning aplicados à Percepção. Sistemas Fuzzy e Neuro-Fuzzy como Controladores. Algoritmos Genéticos. Aprendizado por Reforço Profundo (Deep RL) integrado a sistemas robóticos. Simulação e implementação de Agentes Autônomos.

## 2. OBJETIVOS
- **Geral:** Capacitar o aluno a desenvolver sistemas de controle inteligente onde a "inteligência" (Redes Neurais/Fuzzy/RL) opera como nós de software integrados via middleware ROS 2.
- **Específico:** Preparar os alunos para desenvolver um **Agente Autônomo para Navegação**, utilizando ROS 2 para conectar a percepção visual (PyTorch) ao controle de navegação (RL) em ambientes simulados (Gazebo).

---

## 3. CONTEÚDO PROGRAMÁTICO E CRONOGRAMA INTEGRADO

A disciplina seguirá o fluxo de desenvolvimento de um robô autônomo moderno: **Percepção $\rightarrow$ Decisão $\rightarrow$ Ação**, tudo conectado via ROS 2.

### UNIDADE I: Fundamentos de ROS 2 e Inteligência Computacional (Aulas 1-4)
*O "Sistema Nervoso" do Robô.*
*   **1.1 Introdução ao ROS 2:** Conceitos de Nós, Tópicos, Serviços e Actions. Diferença entre ROS 1 e ROS 2 (DDS middleware).
    *   *Prática:* Instalação do ROS 2 Jazzy e criação de um *workspace*. Criação de um pacote Python com um nó "Talker/Listener" básico.
*   **1.2 Arquitetura de Agentes:** Como estruturar um agente inteligente onde o modelo de IA (PyTorch) é um nó ROS que assina tópicos de sensores e publica em tópicos de velocidade (`cmd_vel`).

### UNIDADE II: Redes Neurais e Percepção Visual no ROS 2 (Aulas 5-10)
*   **2.1 Deep Learning com PyTorch:** Tensores, Autograd e construção de CNNs (ResNet/Custom).
*   **2.2 Integração Visão-Robótica:** Uso do pacote `cv_bridge` para converter mensagens ROS (`sensor_msgs/Image`) para OpenCV/PyTorch.
*   **2.3 Prática de Percepção:**
    *   Simular um robô com câmera no Gazebo.
    *   Criar um nó ROS 2 que assina a câmera, processa a imagem com uma CNN (PyTorch) para classificar objetos ou detectar obstáculos e publica o resultado.

### UNIDADE III: Controle Inteligente Clássico (Fuzzy e Genético) (Aulas 11-15)
*Hibridização e Otimização de Parâmetros.*
*   **3.1 Lógica Fuzzy:** Controladores Fuzzy implementados como nós ROS 2.
    *   *Prática:* Criar um nó "Fuzzy Navigator" que recebe dados do LiDAR (`sensor_msgs/LaserScan`) e ajusta a velocidade para evitar colisões usando regras linguísticas (ex: biblioteca `scikit-fuzzy` ou `fuzzylite` dentro de um nó Python).
*   **3.2 Algoritmos Genéticos (AG):** Uso de AG para otimizar os hiperparâmetros de um controlador ou a arquitetura de uma rede neural (Neuroevolução).


### UNIDADE IV: Aprendizado por Reforço (RL) em Robótica (Aulas 16-23)
*   **4.1 Fundamentos de RL:** MDPs, Agente, Ambiente, Recompensa. Diferença entre RL tabular e Deep RL (DQN/PPO).
*   **4.2 Simulation-to-Real (Sim2Real):** O desafio de treinar em simulação (Gazebo/Isaac Sim) e transferir para o real.
*   **4.3 Prática Integrada (Gymnasium + ROS 2):**
    *   Configurar um ambiente de treino onde o Gazebo é o "Environment".
    *   O Agente (nó ROS 2 com PyTorch) envia ações (`cmd_vel`) e recebe estados (odometria/imagem).
    *   Implementação de DQN ou PPO para navegação sem mapa (Mapless Navigation).

---

## 4. METODOLOGIA DE LABORATÓRIO (30h Práticas)

O laboratório será transformado em um ambiente de desenvolvimento de robótica (R&D). Os alunos trabalharão em **Ubuntu 24.04** (ou via Docker/WSL).

**Projeto Integrador: "O Robô Navegador Inteligente"**
A turma será dividida em equipes para resolver o problema de navegação autônoma em um labirinto simulado no Gazebo.

1.  **Lab 1-2 (Setup):** Instalação do ROS 2, Colcon build, e simulação do **TurtleBot3** ou **Rosbot** no Gazebo.
2.  **Lab 3-4 (Visão/PyTorch):** Coleta de dataset visual via ROS bag. Treinamento offline de uma CNN em PyTorch para identificar "Corredor Livre" vs "Parede".
3.  **Lab 5-6 (Integração):** Criação de um nó de inferência. O robô deve parar automaticamente ao ver uma parede (usando a rede neural, não o LiDAR).
4.  **Lab 7-9 (RL Training):** Implementação de um loop de treinamento RL. O robô deve aprender a sair do labirinto por tentativa e erro. Uso de bibliotecas como **Stable-Baselines3** ou **TorchRL** adaptadas para comunicar via tópicos ROS.
5.  **Lab 10 (Desafio Final):** Competição de navegação. Os robôs (agentes) devem navegar em um cenário inédito.

---

## 5. RECURSOS DIDÁTICOS E BIBLIOGRAFIA

**Softwares Essenciais:**
*   **ROS 2 Jazzy Jalisco:** Middleware de comunicação.
*   **Gazebo Sim (ex-Ignition):** Para simulação física realista.
*   **PyTorch:** Para construção das redes neurais e algoritmos de RL.
*   **Rviz2:** Para visualização dos sensores e do estado do agente.

**Bibliografia Específica:**
1.  **RENARD, Edouard.** *Mastering ROS 2 for Robotics Programming*. 4ª Ed. Packt, 2025. (Crucial para a integração ROS 2 + AI, Capítulos 14 e 15).
2.  **LAPAN, Maxim.** *Deep Reinforcement Learning Hands-On*. 3ª Ed. Packt, 2024. (Base para PPO/DQN e PyTorch).
3.  **GÉRON, Aurélien.** *Hands-On Machine Learning with Scikit-Learn and PyTorch*. O'Reilly, 2025. (Referência para CNNs e treinamento).
4.  **RENARD, Edouard.** *ROS 2 from Scratch*. Packt, 2024. (Para os conceitos fundamentais de nós e tópicos).

