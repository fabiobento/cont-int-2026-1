# Projeto Prático: Operação de Coleta Cooperativa em Turtlesim

## 1. Identificação

* **Disciplina:** Controle Inteligente (Engenharia Elétrica)
* **Instituição:** IFES - Campus Guarapari
* **Ferramentas:** ROS 2 Jazzy, Ubuntu 24.04, Docker, Python 3.12, Turtlesim.
* **Formato:** Grupos de 3 a 4 alunos

## 2. Objetivo do Projeto

Desenvolver um sistema distribuído onde múltiplos nós ROS 2 cooperam para limpar o ambiente simulado. Aplique os conceitos de **Tópicos** (comunicação contínua para percepção) e **Serviços** (comunicação síncrona para eventos/ações) para controlar robôs móveis de forma autônoma.

## 3. Descrição do Cenário (O Problema)

O ambiente do Turtlesim representa uma área de operação industrial. "Resíduos" (outras tartarugas) surgem aleatoriamente no mapa. O grupo deve desenvolver um "Robô Coletor" que:

1. **Percepção:** Descubra a posição do resíduo no mapa.
2. **Decisão:** Calcule a trajetória necessária para atingir o alvo.
3. **Ação:** Movimente-se até o alvo e "colete-o" (remova-o da tela) ao chegar na proximidade.

## 4. Etapas Detalhadas da Atividade

### Fase 1: Orquestração do Ambiente (Docker Compose)

Utilizando o conhecimento da Aula 1 sobre conteinerização , cada grupo deve criar um arquivo `compose.yaml` que suba automaticamente:

* O nó simulador (`turtlesim_node`).
* Um nó de monitoramento (`rqt_graph`).
* O nó controlador em Python que o grupo irá desenvolver.

### Fase 2: Mapeamento de Interfaces (Exploração CLI)

Antes de programar, os alunos devem usar as ferramentas de linha de comando para mapear o sistema :

* Listar tópicos ativos para identificar onde a tartaruga publica sua **Pose** (`/turtle1/pose`).
* Inspecionar o tipo da mensagem para entender os campos `x`, `y` e `theta`.
* Identificar os serviços disponíveis para gerar novos alvos (`/spawn`) e remover alvos atingidos (`/kill`).



### Fase 3: Desenvolvimento do Nó Coletor (Python/rclpy)

Os alunos devem escrever um script Python que utilize a biblioteca de cliente `rclpy` para implementar a lógica de controle inteligente.

**Requisitos do Código:**

* **Assinante (Subscriber):** Monitorar constantemente o tópico de pose da tartaruga principal para saber sua localização atual.
* **Publicador (Publisher):** Enviar comandos de velocidade (`geometry_msgs/msg/Twist`) para o tópico `/cmd_vel`.


* **Cliente de Serviço (Service Client):** Chamar o serviço `/spawn` via código para criar "lixo" em coordenadas aleatórias e o serviço `/kill` para removê-lo quando a distância euclidiana for menor que 0.5 unidades.

### Fase 4: Lógica de Controle Proporcional (P)

Como estudantes de Engenharia Elétrica, os grupos devem implementar um controlador proporcional simples para a velocidade linear :


$$v = K_p \times \text{distância\_até\_o\_alvo}$$


Onde $K_p$ é um ganho que os alunos devem ajustar experimentalmente para evitar oscilações ou colisões com as bordas da tela.

## 5. Dinâmica Cooperativa e Diferenciação

Para garantir a cooperação e o uso avançado de namespaces (conceito de redes ROS 2), o projeto exige:

* **Nó Gerenciador:** Um grupo será responsável por criar um nó que "semeia" alvos para todos os outros grupos.
* **Namespaces:** Cada grupo deve rodar sua tartaruga em um namespace próprio (ex: `/grupo1`, `/grupo2`) para que as tartarugas não recebam comandos umas das outras, mas habitem o mesmo simulador.



## 6. Critérios de Avaliação (Rubrica)

| Critério | Peso | Descrição |
| --- | --- | --- |
| **Integração Docker** | 20% | Sucesso na inicialização via `docker compose` com interface gráfica.
 |
| **Arquitetura ROS 2** | 30% | Uso correto de publicadores, assinantes e serviços distribuídos.
 |
| **Lógica de Controle** | 30% | Precisão do robô em chegar ao alvo sem "atravessar" as bordas (implementação do ganho $K_p$). |
| **Código em Python** | 10% | Organização do script, comentários técnicos e uso da `rclpy`. |
| **Relatório Técnico** | 10% | Descrição do grafo de computação gerado pelo `rqt_graph`. |

## 7. Cronograma Sugerido

1. Configuração do workspace e exploração de serviços/tópicos via terminal.
2. Desenvolvimento do script Python para movimentação básica.
3. Implementação da lógica de coleta (Spawn/Kill) e entrega final.


## 8. Boas Práticas
O projeto deve ser iniciado dentro de um repositório Git (https://github.com/), utilizando boas práticas de desenvolvimento de software.

## 9 . Material de Apoio (Baseado na Aula 1)

* **Comandos Essenciais:** `ros2 run`, `ros2 topic list`, `ros2 service call`.
* **Mensagens:** `turtlesim/msg/Pose` e `geometry_msgs/msg/Twist`.
* **Infraestrutura:** Uso do script `ros2_install_jazzy.sh` e Dockerfiles fornecidos na aula.

