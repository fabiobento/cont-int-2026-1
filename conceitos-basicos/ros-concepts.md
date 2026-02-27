# Aula 2: Primeiros Passos com ROS 2

Na aula anterior, discutimos vários conceitos do ROS 2 que precisamos conhecer antes de começar a programar com ele.

Nesta aula, continuaremos com alguns tópicos que deixamos de fora na aula anterior. Após discutir esses conceitos.

Esta aula ajudará você a construir uma base sólida para implementar diferentes conceitos do ROS 2. Veremos a implementação detalhada desses conceitos, que podem ser aplicados em vários casos de uso na robótica. É fundamental entender todos esses conceitos básicos antes de mergulhar em tópicos mais avançados do ROS 2.

Aqui estão os tópicos importantes que discutiremos nesta aula:

* O que é uma **Action** (ação) no ROS 2?
* O que é um **Parameter** (parâmetro) no ROS 2?
* O que é um **Launch File** (arquivo de inicialização) no ROS 2?
* Como construir um pacote (**Package**) no ROS 2?
* Introdução às bibliotecas de cliente do ROS 2.

## Requisitos Técnicos 

Para acompanhar este roteiro, é recomendável ter um computador ou placa embarcada (por exemplo, Raspberry Pi, placa Jetson, etc.) com o Ubuntu 24.04 LTS instalado ou qualquer outra versão do Ubuntu.

Os materiais de referência para este roteiro podem ser encontrados na pasta `fundamentos-ros2` do seguinte repositório no GitHub: https://github.com/fabiobento/cont-int-2026-1/tree/main/conceitos-basicos.

## ROS 2 Actions: Comunicação para Tarefas de Longa Duração

No ROS 2, uma **Action** (ação) é um protocolo de comunicação projetado para tarefas que não são instantâneas. Enquanto um **Service** segue o modelo síncrono de "pergunta e resposta rápida", a Action é assíncrona e oferece maior controle sobre o processo.

### Por que usar Actions em vez de Services?

| Característica | Service (Serviço) | Action (Ação) |
| --- | --- | --- |
| **Duração** | Curta (ex: ligar um LED) | Longa (ex: navegar 10 metros) |
| **Feedback** | Não possui progresso parcial | Envia atualizações constantes |
| **Cancelamento** | Impossível após a requisição | Pode ser cancelada a qualquer momento |
| **Bloqueio** | Cliente geralmente espera travado | Cliente pode realizar outras tarefas |

### Anatomia de uma Action

Uma Action é composta por três componentes definidos em um arquivo `.action`:

1. **Goal (Objetivo):** A meta enviada pelo *Action Client* (ex: "Vá para a coordenada X,Y").
2. **Feedback (Retorno):** Informações periódicas enviadas pelo *Action Server* durante a execução (ex: "Estou em 50% do caminho").
3. **Result (Resultado):** Resposta final enviada após a conclusão da tarefa (ex: "Cheguei ao destino com sucesso").

### Dinâmica de Funcionamento

* **Action Client:** Inicia a tarefa enviando um objetivo, monitora o progresso via feedback e tem o poder de cancelar a operação.
* **Action Server:** Executa a lógica pesada, publica atualizações de progresso e reporta o desfecho final.

> **Exemplos Práticos:** Navegação autônoma (SLAM), movimentação de juntas em braços robóticos ou sequências complexas de decolagem em drones.

![](https://github.com/fabiobento/cont-int-2026-1/raw/main/conceitos-basicos/imagens/ros-actions.png)

