# Desenvolvimento de Sistemas de Controle Cooperativo Multi-Agente em ROS 2 Jazzy: Projeto Prático para Engenharia Elétrica no IFES Guarapari

O campo da robótica moderna e dos sistemas de controle inteligente tem passado por uma transformação paradigmática com a consolidação de middlewares robustos, como o Robot Operating System 2 (ROS 2), especificamente a distribuição Jazzy Jalisco, otimizada para o Ubuntu 24.04 LTS. No contexto acadêmico do Instituto Federal do Espírito Santo (IFES), campus Guarapari, a disciplina de Controle Inteligente para o curso de Engenharia Elétrica busca integrar conceitos teóricos de automação com ferramentas de nível industrial, preparando os discentes para os desafios da Indústria 4.0 e da robótica móvel autônoma. Após a conclusão da unidade introdutória, documentada na Aula 1, os discentes possuem a base necessária para transitar de execuções simples de nós isolados para a arquitetura de sistemas cooperativos complexos.

O projeto detalhado a seguir, denominado "Desafio de Resgate Cooperativo em Ambiente Simulado", foi estruturado para ser executado por uma turma de 19 alunos, organizados em grupos de três, utilizando a infraestrutura tecnológica já estabelecida em laboratório: computadores equipados com Ubuntu 24.04 e o ecossistema ROS 2 devidamente configurado via Docker. A atividade visa solidificar o entendimento sobre a tríade "Percepção, Decisão e Ação", aplicando algoritmos de controle proporcional e lógica de coordenação multi-agente em Python, dentro do ambiente simulado Turtlesim.

## Fundamentação Teórica e Alinhamento com a Aula 1

A transição da teoria para a prática exige que o discente compreenda o ROS 2 não apenas como um software, mas como o "sistema nervoso" de um robô, onde a conectividade e o fluxo de dados são primordiais. A Aula 1 estabeleceu os requisitos técnicos para o desenvolvimento, focando na instalação nativa e conteinerizada do ROS 2 Jazzy, além da exploração inicial de ferramentas como o simulador Turtlesim e bibliotecas de cliente rclpy. O projeto cooperativo expande esses conceitos ao exigir que múltiplos agentes interajam em um mesmo espaço de estados, forçando a implementação de namespaces, remapeamento de tópicos e o uso avançado de serviços e ações.

### O Middleware ROS 2 como Infraestrutura de Controle

A escolha do ROS 2 Jazzy como padrão para a disciplina justifica-se por sua arquitetura baseada no Data Distribution Service (DDS), que oferece segurança e determinismo na comunicação entre processos (IPC). Para futuros engenheiros eletricistas, compreender a camada de middleware é fundamental, pois é nela que se define a qualidade da sincronia entre sensores e atuadores. No projeto, a comunicação assíncrona via tópicos e a comunicação síncrona via serviços serão testadas em um cenário onde a latência pode comprometer a eficácia do algoritmo de controle.

A infraestrutura de laboratório do IFES Guarapari, focada no Ubuntu 24.04, permite a exploração plena das capacidades do Jazzy, incluindo melhor suporte para Python 3.12 e integração com o ecossistema de Inteligência Artificial via PyTorch, que será o foco de módulos futuros da disciplina. O uso de Docker e Docker Compose, já introduzidos, torna-se a espinha dorsal para a orquestração dos múltiplos nós necessários para a coordenação de uma frota de robôs simulados.

## Descrição do Projeto: Desafio de Resgate Cooperativo

O projeto consiste no desenvolvimento de uma aplicação multi-agente onde três robôs (tartarugas) devem cooperar para "resgatar" alvos (outras tartarugas) que surgem aleatoriamente no ambiente simulado. A coordenação deve evitar que dois robôs persigam o mesmo alvo e garantir que a bateria de cada agente (simulada por um contador de distância) seja gerida de forma inteligente.

### Cenário e Regras de Operação

A turma de 19 alunos será dividida em 6 grupos de 3 alunos, com um aluno assumindo um papel de coordenação técnica inter-grupos ou integrando-se a um grupo específico sob regime de monitoria. Cada grupo será responsável por desenvolver sua própria frota cooperativa dentro de um container Docker isolado, simulando um ecossistema de robôs autônomos.

As especificações do ambiente de simulação e as regras de controle seguem parâmetros técnicos rigorosos para garantir a validade acadêmica do exercício:

| Parâmetro | Especificação Técnica | Relevância para o Controle |
| --- | --- | --- |
| **Sistema Operacional** | Ubuntu 24.04 LTS (Noble Numbat) | Estabilidade de drivers e suporte LTS.

 |
| **Distribuição ROS** | ROS 2 Jazzy Jalisco | Uso de DDS moderno e suporte a Python 3.12.

 |
| **Simulador** | Turtlesim (turtlesim_node) | Visualização 2D de cinemática diferencial.

 |
| **Linguagem** | Python (rclpy) | Rapidez de prototipagem para algoritmos de IA.

 |
| **Gestão de Processos** | Docker Compose | Orquestração de múltiplos nós e rede isolada.

 |
| **Tipo de Controle** | Malha Fechada (Proporcional) | Estabilidade de navegação ponto-a-ponto.

 |

O desafio exige que os alunos criem três nós principais: um "Nó Spawner" (Gerenciador de Alvos), um "Nó Coordenador" (Estrategista) e o "Nó Agente" (Controlador de Movimento), que será instanciado três vezes, uma para cada robô da frota.

### A Arquitetura de Software Multi-Nó

A arquitetura proposta para o projeto baseia-se na modularidade incentivada pelo ROS 2. Em vez de um único script monolítico, os alunos devem desenvolver um pacote Python que contenha diferentes executáveis, cada um com uma responsabilidade bem definida no grafo de computação.

1. **Nó Spawner (`turtle_spawner`)**: Este nó utiliza o serviço `/spawn` do Turtlesim para criar tartarugas "alvos" em coordenadas $(x, y)$ aleatórias em intervalos regulares. Ele deve manter uma lista interna de alvos "vivos" no sistema e publicá-la em um tópico personalizado chamado `/targets_list` utilizando uma interface de mensagem customizada (`.msg`).


2. **Nó Coordenador (`fleet_manager`)**: Atuando como o cérebro estratégico, este nó assina o tópico `/targets_list` e monitora a pose de todos os robôs da frota. Ele utiliza algoritmos de decisão simples (como a distância euclidiana mínima) para atribuir alvos específicos a robôs específicos através de um serviço customizado chamado `/assign_target`.


3. **Nó Agente (`turtle_controller`)**: Instanciado três vezes com namespaces diferentes (`/robot1`, `/robot2`, `/robot3`), este nó assina sua própria pose (`/pose`) e recebe comandos de destino do coordenador. Ele implementa um controlador proporcional para calcular as velocidades linear e angular necessárias para atingir o alvo.



## Implementação da Infraestrutura Docker e Orquestração

Conforme estabelecido na Aula 1, o desenvolvimento moderno de robótica não deve depender exclusivamente de instalações locais que possam "quebrar" o sistema hospedeiro. Portanto, o projeto exige que os alunos construam e gerenciem seus próprios ambientes via Docker.

### O Dockerfile como Receita de Ambiente

Cada grupo deve aprimorar o `Dockerfile` apresentado na aula inicial para incluir as dependências necessárias para o projeto cooperativo. Isso inclui não apenas o ROS 2 Jazzy em sua versão `desktop-full`, mas também pacotes adicionais de Python para cálculos matemáticos e visualização de dados.

A narrativa técnica da construção da imagem deve seguir estas etapas:

* **Seleção da Imagem Base**: Utilizar `osrf/ros:jazzy-desktop-full` para garantir que o simulador Turtlesim e as ferramentas `rviz2` e `rqt` estejam presentes.


* **Criação de Usuário não-root**: Por questões de segurança e compatibilidade com ferramentas gráficas, é essencial criar um usuário `robot` com os mesmos IDs (UID/GID) do host Ubuntu 24.04.


* **Instalação de Dependências**: Utilizar o comando `RUN apt install` para adicionar `ros-jazzy-turtlesim` e ferramentas de build como `python3-colcon-common-extensions`.


* **Configuração do Workspace**: O diretório de trabalho deve ser montado como um volume para que o código Python desenvolvido pelos alunos no host seja refletido instantaneamente dentro do container.



### Orquestração com Docker Compose

Dada a natureza multi-agente do projeto, o uso do Docker Compose é obrigatório para gerenciar a rede e a inicialização dos nós. O arquivo `compose.yaml` deve definir serviços separados para o simulador, o coordenador e os agentes. Isso permite que os alunos testem a resiliência do sistema: o que acontece se o coordenador cair enquanto as tartarugas estão em movimento?.

A configuração do `compose.yaml` deve contemplar:

* **Rede Isolada**: Todos os containers devem pertencer à mesma rede Docker para que o DDS do ROS 2 possa descobrir os nós automaticamente sem interferir em outros grupos no laboratório.


* **Persistência de Dados**: Volumes montados para as pastas de código e logs.


* **Habilitação de GUI**: Configurações de variáveis de ambiente como `DISPLAY` e montagem do socket do X11 ou Wayland para permitir que a janela do Turtlesim seja exibida no monitor do computador do IFES.



## Desenvolvimento do Sistema de Controle em Python

O núcleo de engenharia do projeto reside no desenvolvimento dos controladores em malha fechada. Os alunos de Engenharia Elétrica devem aplicar os conceitos de sistemas de controle para garantir que as tartarugas se movam de forma suave e precisa.

### O Controlador Proporcional para Navegação

Cada nó agente deve implementar uma lógica de controle baseada no erro de posição. Ao receber um alvo $(x_{goal}, y_{goal})$, o robô deve calcular continuamente sua distância euclidiana e o ângulo em relação ao alvo :

A distância linear ($d$) e o ângulo de erro ($\alpha$) são definidos matematicamente como:


$$d = \sqrt{(x_{goal} - x_{current})^2 + (y_{goal} - y_{current})^2}$$

$$\alpha = \operatorname{atan2}(y_{goal} - y_{current}, x_{goal} - x_{current}) - \theta_{current}$$

O comando de velocidade linear ($v$) e angular ($\omega$) enviado ao tópico `/cmd_vel` será:


$$v = K_p \cdot d$$

$$\omega = K_a \cdot \alpha$$

Onde $K_p$ e $K_a$ são os ganhos proporcionais que os alunos devem ajustar experimentalmente. Valores muito altos de $K_a$ causarão oscilações violentas, enquanto valores muito baixos resultarão em curvas muito abertas, podendo levar a colisões com as bordas do simulador.

### Lógica Cooperativa e Gestão de Missão

A inteligência do sistema cooperativo é testada na forma como os robôs decidem quem busca qual alvo. O nó `fleet_manager` deve implementar uma lógica de atribuição de tarefas que evite conflitos.

| Estratégia de Cooperação | Descrição Técnica | Vantagem para o Projeto |
| --- | --- | --- |
| **Nearest Neighbor** | Cada robô escolhe o alvo mais próximo de sua posição atual.

 | Simplicidade de implementação e baixo custo computacional. |
| **Task Queue** | O coordenador mantém uma fila de alvos e os atribui conforme os robôs ficam livres.

 | Garante que todos os alvos sejam resgatados na ordem de surgimento. |
| **Namespacing** | Cada robô opera em seu próprio namespace (`/turtle1`, `/turtle2`).

 | Evita colisão de mensagens e permite escalabilidade da frota. |

Os alunos devem utilizar o padrão de serviço (`Service`) do ROS 2 para a atribuição de tarefas. Diferente dos tópicos, o serviço garante que o robô agente recebeu a meta com sucesso (confirmação síncrona), o que é vital para o controle de estado da missão.

## Implementação Avançada: Comportamentos e Estados

Para elevar o nível do projeto de "Controle Básico" para "Controle Inteligente", os grupos são encorajados a implementar uma máquina de estados simples ou Árvores de Comportamento (Behavior Trees) para gerir a vida útil dos robôs.

### Simulação de Bateria e Estação de Carga

Cada robô agente deve possuir um parâmetro interno de "bateria". A energia é consumida proporcionalmente à velocidade linear e angular.

* **Estado de Operação**: O robô resgata alvos normalmente.
* **Estado de Alerta**: Quando a bateria atinge 20%, o robô interrompe sua missão atual e deve navegar até uma "estação de recarga" fixa (ex: coordenada $1, 1$).


* **Estado de Recarga**: O robô permanece parado por 10 segundos na estação até que a bateria retorne a 100%.

Essa lógica introduz o conceito de priorização de tarefas e gerenciamento de recursos, fundamentais em sistemas autônomos industriais. Os alunos utilizarão o sistema de parâmetros do ROS 2 para configurar os limites de bateria e as taxas de consumo sem precisar recompilar o código.

### Transformações de Coordenadas com TF2

Embora o Turtlesim utilize um sistema de coordenadas global, a introdução da biblioteca `tf2` é essencial para que os alunos compreendam como robôs lidam com sensores relativos. Os alunos devem configurar um `StaticTransformBroadcaster` para a estação de carga e um `TransformBroadcaster` dinâmico para cada tartaruga. Isso permitirá que eles usem ferramentas como o `tf2_echo` para verificar a distância entre robôs no sistema de coordenadas de outros robôs, um conceito chave para evitar colisões no futuro.

## Metodologia de Execução no Laboratório do IFES

A turma de 19 alunos apresenta um desafio logístico que requer organization clara do tempo e dos recursos. A atividade será dividida em três sessões de laboratório de 4 horas cada.

### Cronograma de Atividades

| Sessão | Atividade Principal | Entregável Esperado |
| --- | --- | --- |
| **1: Infraestrutura** | Configuração do Docker Compose e criação dos nós Spawner e Agente básico. | Grafo do ROS 2 funcional com 3 robôs parados e alvos surgindo. |
| **2: Controle** | Implementação e sintonia dos ganhos do controlador proporcional P em Python. | Robôs navegando individualmente até coordenadas fixas sem oscilação. |
| **3: Cooperação** | Integração do Fleet Manager e lógica de atribuição de tarefas/recarga. | Sistema cooperativo completo operando de forma autônoma. |

Cada computador do laboratório servirá como a "estação de comando" de uma frota. Os alunos utilizarão o VS Code com a extensão de "Dev Containers" para editar o código diretamente dentro do ambiente Docker, uma técnica industrial que facilita o debug e garante que todos os membros do grupo trabalhem no mesmo ambiente exato.

### O Papel do Ubuntu 24.04 e Performance

O Ubuntu 24.04 fornece o kernel 6.8, que melhora a gestão de processos e o suporte a hardware moderno. Os alunos observarão que o uso do ROS 2 Jazzy sobre esta base permite uma comunicação mais estável, especialmente ao utilizar o RMW (ROS MiddleWare) padrão, o CycloneDDS. Em aulas posteriores, eles poderão comparar a performance do CycloneDDS com o FastDDS em cenários de alta carga de dados de sensores simulados.

## Avaliação e Critérios de Sucesso

A avaliação não se limitará ao funcionamento visual da simulação, mas abrangerá a qualidade técnica da solução de engenharia. Uma rubrica detalhada será utilizada para garantir transparência e rigor acadêmico.

### Rubrica de Avaliação (Escala de 0 a 100)

* **Arquitetura de Sistemas (30 pts)**: Uso correto de Namespaces, Services e Topics. O sistema deve ser modular e resiliente a falhas de nós individuais.


* **Estabilidade do Controle (25 pts)**: Os robôs devem atingir os alvos com um erro de estado estacionário inferior a 0.2 unidades e sem ultrapassagem (overshoot) significativa.


* **Implementação Docker (20 pts)**: O projeto deve ser iniciado com um único comando `docker compose up`. O Dockerfile deve ser otimizado e bem documentado.


* **Coordenação e Inteligência (15 pts)**: Eficácia na divisão de tarefas e gestão do comportamento de bateria/recarga.


* **Qualidade do Código Python (10 pts)**: Aderência às normas PEP 8, comentários técnicos claros e uso eficiente das APIs da biblioteca `rclpy`.



### Documentação e Relatório Técnico

Além do código-fonte hospedado em um repositório Git (preferencialmente GitHub ou GitLab do IFES), os grupos devem entregar um relatório técnico detalhando:

1. O cálculo dos ganhos $K_p$ e $K_a$ e a justificativa para os valores escolhidos.
2. Um diagrama do grafo de computação gerado pelo `rqt_graph`.


3. Uma análise de "pior caso": o que acontece com a coordenação se a rede Docker sofrer latência ou se um robô "morrer" no meio do trajeto.

## Conclusão e Perspectiva Futura

Este projeto cooperativo no IFES Guarapari representa o fechamento do primeiro ciclo da disciplina de Controle Inteligente. Ao dominar a orquestração de múltiplos agentes em ROS 2 Jazzy, os alunos saem da zona de conforto da automação sequencial tradicional e entram no domínio dos sistemas ciber-físicos distribuídos.

A experiência adquirida com o Turtlesim e o Docker prepara o terreno para os próximos desafios da disciplina, que incluirão o uso do simulador 3D Gazebo, a integração de câmeras virtuais com OpenCV para visão computacional e, finalmente, a substituição dos controladores proporcionais clássicos por agentes de Aprendizado por Reforço (Reinforcement Learning) e Redes Neurais Profundas. O sucesso desta atividade valida a abordagem prática e acessível proposta pelo curso, alinhando o ensino da Engenharia Elétrica às demandas tecnológicas globais contemporâneas.