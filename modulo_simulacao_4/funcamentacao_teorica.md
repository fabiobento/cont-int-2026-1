# Aula 7: Fundamentação Teórica - Deep Reinforcement Learning no ROS 2

## **Introdução**
Programar robôs para lidar com a natureza imprevisível do mundo real e gerar os sinais de controle corretos para as ações desejadas pode ser complexo. Recentemente, o aprendizado por reforço profundo (DRL - *Deep Reinforcement Learning*) surgiu como uma abordagem poderosa, especialmente para controlar robôs com muitos graus de liberdade, como humanoides ou quadrúpedes. O DRL permite que os robôs aprendam a se mover de forma eficaz para realizar tarefas específicas. Nesta aula, exploraremos duas ferramentas fundamentais para o aprendizado por reforço profundo, ou seja, o `gymnasium` e a `stable_baselines3`. Aplicaremos essas ferramentas para resolver um problema de controle clássico, o pêndulo invertido (*cart-pole*). Uma parte crítica do DRL é a simulação, que é comumente usada para treinar modelos de robôs. Conectaremos essas ferramentas de DRL ao Gazebo para treinar e testar o modelo do *cart-pole* em simulação.

## **Estrutura**
Nesta aula, os seguintes tópicos serão abordados:

* Introdução ao Aprendizado por Reforço Profundo (DRL)
* DRL e Robótica
* Controle de um Robô Usando Valores de Torque
* Introdução ao Framework Gymnasium
* Configuração do Cenário de Simulação do Cart-Pole
* Integração do Gymnasium com o ROS 2
* Treinamento de um Robô usando Gymnasium e stable_baselines3
* Controle de um Robô usando Aprendizado por Reforço Profundo

## **Introdução ao Aprendizado por Reforço Profundo (DRL)**
O aprendizado de máquina transformou a robótica, permitindo que os robôs percebam a complexidade do ambiente e executem tarefas complexas de forma autônoma, adaptem-se a ambientes em mudança e aprendam com a experiência. Em futuras aulas veremos, pelo menos, duas aplicações de Inteligência Artificial (mais especificamente de Aprendizado de Máquina):

* *Visão Computacional usando ROS 2*: usaremos um sistema de Rede Neural Profunda para extrair informações semânticas de um fluxo de vídeo de uma câmera.
* *Uso de Modelos de Linguagem Grande com ROS 2*: usaremos os Modelos de Linguagem Grande (*Large Language Models* - LLMs) que exploram arquiteturas de Aprendizado Profundo para interagir com um robô de uma forma mais natural.

Nesta aula, veremos como o robô pode aprender com sua experiência para executar melhor as ações de movimento.

**Nota:** A Inteligência Artificial (IA) é um campo mais amplo focado na criação de máquinas que executam tarefas que exigem inteligência semelhante à humana, como raciocínio e resolução de problemas. O Aprendizado de Máquina (ML - *Machine Learning*) é um subconjunto da IA que permite que os sistemas aprendam com os dados e melhorem sem programação explícita. A IA abrange uma ampla gama de técnicas, enquanto o ML foca especificamente no reconhecimento de padrões e na tomada de decisões através de modelos guiados por dados.

Vamos começar introduzindo as diferentes abordagens do Aprendizado de Máquina e da Robótica:

* **Aprendizado Supervisionado:** Os robôs são treinados em dados rotulados para realizar tarefas como reconhecimento de objetos, classificação e imitação de movimento. Esta abordagem é eficaz quando grandes conjuntos de dados rotulados estão disponíveis, mas pode não generalizar bem para novos ambientes.
* **Aprendizado Não Supervisionado:** Os robôs utilizam aprendizado não supervisionado para descobrir padrões em dados não rotulados, auxiliando na extração de características, agrupamento (*clustering*) e exploração autônoma. Isso ajuda os robôs a entenderem seu ambiente sem supervisão explícita, mas pode exigir interpretação adicional para aplicação em tarefas específicas.
* **Aprendizado por Imitação:** Os robôs aprendem observando demonstrações de especialistas, replicando comportamentos sem exigir funções de recompensa explícitas. Esta abordagem é útil para tarefas onde as demonstrações são mais fáceis do que definir sistemas de recompensa complexos, como tarefas de manipulação e controle.
* **Aprendizado por Reforço (RL):** Os robôs aprendem por tentativa e erro, otimizando ações com base em recompensas. O RL é ideal para tarefas de tomada de decisão, como navegação autônoma e manipulação robótica, onde a programação explícita é desafiadora. O RL Profundo aproveita as redes neurais para espaços complexos de estados e ações, mas geralmente requer grandes recursos computacionais.

Este último tópico descreve o tema desta aula. Em particular, estudaremos uma aplicação típica do Aprendizado por Reforço Profundo (DRL). O Aprendizado por Reforço Profundo é uma combinação de aprendizado por reforço (RL) e aprendizado profundo (DL - *Deep Learning*). O objetivo do DRL é treinar um agente para tomar uma sequência de decisões aprendendo com as interações com um ambiente, onde as ações afetam estados futuros e recompensas. Esse processo é representado na Figura 1. 

<a id="figure-19-2"></a>
![](https://github.com/fabiobento/dnn-course-2026-1/raw/main/images/figure-19-2.png)

**Figura 1 - Aprendizado por reforço usando uma política de rede neural (*neural network policy*).** ([Fonte](https://ageron.github.io/))


Os componentes centrais de um sistema de DRL (*Deep Reinforcement Learning* - Aprendizado por Reforço Profundo) são descritos a seguir:

* **Agente (*Agent*):** O aprendiz ou tomador de decisão que interage com o ambiente.
* **Ambiente (*Environment*):** O mundo ou sistema com o qual o agente interage, onde os estados evoluem com base nas ações do agente.
* **Observação ou Estado (*Observation or State*) (s):** A condição atual ou representação do ambiente. O estado fornece ao agente as informações necessárias para tomar decisões.
* **Ação (*Action*) (a):** As decisões que o agente toma, as quais afetam o ambiente e levam a transições para novos estados.
* **Recompensa (*Reward*) (r):** O retorno que o agente recebe após cada ação. O objetivo é maximizar as recompensas cumulativas ao longo do tempo.
* **Política (*Policy*) (π):** A estratégia ou o mapeamento de observações para ações que o agente segue para maximizar as recompensas. A política pode ser determinística (fixa para cada estado) ou estocástica (uma distribuição de probabilidade sobre as ações).

No DRL, o agente explora o ambiente para descobrir quais ações rendem as recompensas mais altas (exploração), ao mesmo tempo em que usa as informações que já conhece para maximizar as recompensas (explotação). O equilíbrio entre os dois é fundamental para o aprendizado. Esse processo é chamado de Exploração versus Explotação. Para aprender como executar as ações, a cada iteração o agente observa o ambiente e toma uma ação baseada em sua política, ou de forma aleatória se a política tiver poucas amostras. Ele executa a ação, move-se para um novo estado, recebe uma recompensa e atualiza sua política ou função de valor para melhorar as decisões futuras.

Como você pode imaginar, o DRL se inspira no processo de aprendizado humano. Assim como os humanos, os agentes de DRL aprendem por tentativa e erro, recebendo *feedback* (recompensas ou penalidades) por suas ações e ajustando o comportamento futuro para maximizar o sucesso a longo prazo.

Isso reflete como as pessoas aprendem com as experiências e consequências para melhorar a tomada de decisões ao longo do tempo. No entanto, diferente dos humanos, o DRL se baseia em estruturas matemáticas, requer muito mais dados para aprender de forma eficaz e carece das habilidades cognitivas inatas que os humanos possuem para raciocínio e generalização. Na verdade, o processo de funcionamento do DRL é baseado no uso de Redes Neurais Profundas (*Deep Neural Networks* - DNN) para criar a política usada pelo agente para selecionar as próximas ações. Antes de passarmos para uma implementação prática de um exemplo de DRL, vamos rever brevemente quais são as principais aplicações do DRL e da robótica.

**Nota:** Em suma, uma rede neural é um modelo computacional inspirado na estrutura biológica do cérebro, composto por camadas de neurônios interconectados que processam informações e aprendem padrões a partir de dados. Uma rede neural profunda (DNN) é uma rede neural com muitas camadas ocultas, o que lhe permite aprender padrões mais complexos.

### DRL e Robótica

O DRL encontrou várias aplicações no campo da robótica. Entre os diferentes usos, as seguintes aplicações robóticas se beneficiam fortemente do DRL:

* **Manipulação (*Grasping*):** Robôs industriais operando em setores de serviços se beneficiam do DRL para manipulação de objetos, preensão e controle motor fino. O DRL permite que o robô se adapte a novas formas e posições de objetos em tempo real.
* **Locomoção com Pernas (*Legged Locomotion*):** O DRL é altamente eficaz no controle de robôs com muitos graus de liberdade, como robôs humanoides ou quadrúpedes, aprendendo estratégias otimizadas para caminhar, correr ou escalar.
* **Controle Dinâmico de Robôs:** Envolve gerar entradas de controle que levam em conta as propriedades físicas de um robô (por exemplo, massa, inércia e atrito) para alcançar movimentos e comportamentos desejados. O Aprendizado por Reforço Profundo tem uma forte conexão com o controle dinâmico, pois pode aprender a otimizar ações que lidam com a física complexa dos robôs sem a necessidade de uma modelagem precisa da dinâmica. Esse elemento é importante porque, tipicamente, obter modelos dinâmicos precisos não é trivial. Além disso, isso o torna poderoso para lidar com comportamentos dinâmicos complexos em robôs, especialmente quando a dinâmica é difícil de modelar ou prever.

Considere o controle do movimento de um robô quadrúpede, que normalmente tem 12 ou mais articulações. Para usar o controle tradicional, você precisa calcular ou gerar um modelo cinemático e dinâmico a partir do URDF do robô e projetar uma lei de controle que leve em conta todos os parâmetros dinâmicos. Em contraste, com um controlador baseado em DRL, você só precisa configurar o ambiente para o treinamento. O DRL também permite testar diferentes condições de operação durante o treinamento. Por exemplo, você pode treinar o quadrúpede para lidar com pisos de diferentes níveis de escorregamento, tornando-o capaz de operar em ambientes desafiadores. Com o controle baseado em modelos, se o sistema não estiver devidamente ajustado, as mudanças no ambiente podem causar problemas para o robô. Por outro lado, o DRL às vezes pode ser um exagero. Se você estiver trabalhando com um sistema simples que opera consistentemente no mesmo ambiente, as abordagens clássicas de controle baseadas em modelos são mais do que suficientes e eficientes.

Uma pergunta comum é: como podemos executar várias tentativas do movimento de um robô sem o risco de danos, se o agente ainda não aprendeu a se comportar? A resposta é simples: use um simulador.
Os simuladores fornecem um ambiente controlado, seguro e rápido onde os robôs podem aprender, acelerando o desenvolvimento e a implantação de algoritmos de DRL para uso no mundo real. Além disso, você pode treinar vários agentes simultaneamente dentro de uma simulação, reduzindo o tempo geral de treinamento.
No entanto, nem todos os simuladores são adequados para o treinamento de agentes de DRL. Um requisito fundamental é um motor de física realista e a fidelidade da simulação comparada ao robô real. Por exemplo, no DRL, uma entrada de controle comum é o torque. Para transferir uma política aprendida da simulação para um robô real, os torques simulados devem corresponder de perto às condições do mundo real. Se as magnitudes do torque forem incompatíveis, a política não será útil na prática. Vamos discutir melhor o que significa controlar um robô usando valores de torque.

### Controlando um Robô Usando Valores de Torque

Nos exemplos anteriores de Controle Inteligente, nós controlamos as estruturas robóticas principalmente em posição ou velocidade. Outro modo de controle que pode ser encontrado na robótica é o modo de controle de torque (ou esforço). Quando controlamos um robô usando torques, podemos controlar diretamente a força rotacional aplicada aos seus motores. Diferente do controle de posição ou velocidade, onde o foco é atingir um ângulo ou velocidade específica, o controle de torque comanda diretamente a força aplicada. 

A principal vantagem do controle de torque é sua capacidade de lidar com tarefas dinâmicas e interagir naturalmente com o ambiente, fornecendo regulação fina de força. Isso permite um comportamento adaptativo, particularmente em sistemas complexos, como robôs humanoides ou quadrúpedes. No entanto, o controle de torque apresenta desafios. É mais complexo de projetar e ajustar comparado aos métodos de controle tradicionais e pode exigir *hardware* especializado, como sensores de torque precisos e atuadores responsivos. Além disso, o controle de torque é menos preciso para tarefas que exigem posicionamento exato e pode ser sensível ao ruído do sensor ou à instabilidade do sistema. Para sistemas mais simples ou tarefas em ambientes estáticos, o controle de posição ou velocidade pode ser mais eficiente. No entanto, em cenários onde o controle de força em tempo real e a adaptabilidade são críticos, o controle de torque oferece benefícios significativos, especialmente quando combinado com o aprendizado por reforço profundo para ambientes onde os robôs precisam aprender e se adaptar a novas condições.

Os métodos de DRL podem trabalhar com qualquer tipo de entrada de controle, incluindo controle de posição e velocidade. No entanto, a escolha do método de controle depende da aplicação específica e do tipo de entrada que o robô requer para atuação.

Agora que introduzimos o problema associado ao Aprendizado por Reforço Profundo, vamos ver um dos *frameworks* mais usados para implementar as principais funções necessárias para realizar a tarefa de aprendizado: o Gymnasium.

### Apresentando o Framework Gymnasium

O Gymnasium é um kit de ferramentas Python projetado para desenvolver algoritmos de Aprendizado por Reforço. Ele é o sucessor do famoso kit de ferramentas chamado Gym. A ideia central do Gymnasium é oferecer uma interface consistente que simplifique a interação entre o robô (o agente) e um ambiente (a tarefa ou problema a ser resolvido). Isso torna mais fácil para os usuários se concentrarem em construir e refinar seus algoritmos sem se preocuparem com as complexidades do design do ambiente ou configuração da tarefa.

Lembre-se que o Gymnasium por si só não oferece nenhum procedimento de treinamento ou teste para nossos agentes, apenas as funções para implementar o ambiente. Aprenderemos como usar o ambiente definido aqui para treinar um agente. De fato, o principal uso do Gymnasium é a definição do chamado ambiente de treinamento (o "ginásio" onde nosso robô pode se exercitar bastante!). Junto com a possibilidade de definir seu ambiente, o Gymnasium oferece vários ambientes que podem ser usados para treinar agentes, como um pêndulo invertido ou um *cart-pole* (o mesmo discutido neste capítulo), ou treinar personagens para jogar vários jogos antigos de Atari ([https://ale.farama.org/environments/](https://ale.farama.org/environments/) ).

Em termos simples, criar um ambiente no Gymnasium envolve definir todas as funções que o agente usará para aprender e completar tarefas específicas. É função do desenvolvedor desenhar essas funções com cuidado, identificando as variáveis-chave que impactam o processo de aprendizado. Quanto melhores e mais eficientes forem essas funções, mais rápido e efetivamente o agente aprenderá a executar a tarefa. As funções mais importantes envolvidas no treinamento dos agentes são descritas a seguir:

* **step:** Atualiza o ambiente com base em uma ação, retornando a próxima observação (ou estado) para o agente, a recompensa associada à ação e se o ambiente terminou (seja por terminação ou truncamento). Quando a terminação acontece, um episódio de treinamento termina.
* **reset:** Reinicia o ambiente para o seu estado inicial e é obrigatório antes de invocar `step()`. Ele fornece a primeira observação do agente para o episódio e informações complementares, como métricas ou dados de depuração. A função de *reset* é invocada quando um episódio termina.
* **close:** Este método encerra o ambiente, o que é crucial quando *softwares* externos estão envolvidos e devem ser encerrados de forma limpa.

Note que essas funções não estão diretamente ligadas a nenhum recurso que forneça informações sobre o status do robô ou onde as ações selecionadas são aplicadas. Ao usar o ambiente fornecido no pacote, você pode conectá-lo a um sistema de renderização ou ao simulador MuJoCo. Adicionalmente, definir um ambiente envolve vincular as entradas e saídas com as quais o agente interage. No nosso exemplo, conectaremos o ambiente ao Gazebo. Antes de integrá-lo ao ROS 2 através do Gazebo, 

Você pode usar os módulos do Gymnasium em um script Python para definir um novo ambiente. No entanto, antes de fazer isso, precisamos criar um modelo de simulação. Este modelo deve imitar o sistema real o mais fielmente possível; caso contrário, ao transferir o modelo treinado para o sistema real (*sim-to-real*), as ações podem não se comportar como o esperado, levando à falha da tarefa.

**Nota:** O *sim-to-real* é o processo de transferir modelos treinados em simulação para aplicações no mundo real. Ele visa preencher a "lacuna da realidade" (*reality gap*), garantindo que o modelo funcione efetivamente em ambos os ambientes, apesar das diferenças.

Vamos começar definindo o modelo de simulação do *cart-pole*.

## **Configurando o Cenário de Simulação do Cart-Pole**

Um sistema *cart-pole* (pêndulo invertido) é um exemplo clássico na teoria de controle e no aprendizado por reforço, usado para demonstrar tarefas de equilíbrio e controle. Ele consiste em um carrinho que pode se mover ao longo de um trilho e uma haste (pêndulo) presa ao carrinho por um pivô (veja a Figura 16.2). O objetivo é aplicar forças ao carrinho para manter a haste equilibrada na posição vertical. O sistema é comumente usado como um problema de referência (*benchmark*) em aprendizado por reforço para testar algoritmos de controle, onde o agente deve aprender a impedir que a haste caia movendo o carrinho para a esquerda ou para a direita. Como queremos integrar o Cart-Pole com o ROS 2, definiremos o modelo do robô configurando o *plugin* `ros2_control`.