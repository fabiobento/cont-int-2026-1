# Aula 7: Fundamentação Teórica - Deep Reinforcement Learning no ROS 2

## **Introdução**
Programar robôs para lidar com a natureza imprevisível do mundo real e gerar os sinais de controle corretos para as ações desejadas pode ser complexo. Recentemente, o aprendizado por reforço profundo (DRL - *Deep Reinforcement Learning*) surgiu como uma abordagem poderosa, especialmente para controlar robôs com muitos graus de liberdade, como humanoides ou quadrúpedes. O DRL permite que os robôs aprendam a se mover de forma eficaz para realizar tarefas específicas. Nesta aula, exploraremos duas ferramentas fundamentais para o aprendizado por reforço profundo, ou seja, o [Gymnasium](https://gymnasium.farama.org/index.html) e a [Stable-Baselines3](https://stable-baselines3.readthedocs.io/en/master/). Aplicaremos essas ferramentas para resolver um problema de controle clássico, o pêndulo invertido (*cart-pole*). Uma parte crítica do DRL é a simulação, que é comumente usada para treinar modelos de robôs. Conectaremos essas ferramentas de DRL ao Gazebo para treinar e testar o modelo do *cart-pole* em simulação.

## **Estrutura**
Nesta aula, os seguintes tópicos serão abordados:

* Introdução ao Aprendizado por Reforço Profundo (*Deep Reinforcement Learning* - DRL)
* DRL e Robótica
* Controle de um Robô Usando Valores de Torque
* Introdução ao Framework [Gymnasium](https://gymnasium.farama.org/index.html) 
* Configuração do [Cenário de Simulação do Cart-Pole](https://gymnasium.farama.org/environments/classic_control/cart_pole/)
* Integração do Gymnasium com o [ROS 2](https://www.ros.org/)
* Treinamento de um Robô usando Gymnasium e [Stable-Baselines3](https://stable-baselines3.readthedocs.io/en/master/)
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

<a id="figure-1"></a>
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

Um sistema *cart-pole* (pêndulo invertido) é um exemplo clássico na teoria de controle e no aprendizado por reforço, usado para demonstrar tarefas de equilíbrio e controle. Ele consiste em um carrinho que pode se mover ao longo de um trilho e uma haste (pêndulo) presa ao carrinho por um pivô (veja a Figura 2). O objetivo é aplicar forças ao carrinho para manter a haste equilibrada na posição vertical. O sistema é comumente usado como um problema de referência (*benchmark*) em aprendizado por reforço para testar algoritmos de controle, onde o agente deve aprender a impedir que a haste caia movendo o carrinho para a esquerda ou para a direita. Como queremos integrar o Cart-Pole com o ROS 2, definiremos o modelo do robô configurando o *plugin* `ros2_control`.

<a id="figure-2"></a>
![](https://raw.githubusercontent.com/fabiobento/cont-int-2026-1/main/modulo_simulacao_4/imagens/cart-pole.png)

**Figura 2 - O pêndulo invertido usado na aplicação de DRL.** 

Vamos começar criando um pacote ROS 2 para armazenar o modelo e os arquivos de simulação(você pode encontrar uma cópia do pacote [`cartpole_description` nesse link](https://github.com/fabiobento/cont-int-2026-1/tree/main/modulo_simulacao_4/scripts/cartpole_description).

```bash
$ ros2 pkg create cartpole_description
```

Este pacote conterá o modelo [*xacro*](https://github.com/fabiobento/cont-int-2026-1/blob/main/modulo_simulacao_4/scripts/cartpole_description/urdf/cartpole.urdf.xacro) do robô e um arquivo [*launch*](https://github.com/fabiobento/cont-int-2026-1/blob/main/modulo_simulacao_4/scripts/cartpole_description/launch/cartpole.launch.py) que inicia a simulação e os diferentes controladores. O arquivo do modelo é básico e consiste em duas juntas:

* **linear:** Uma junta prismática para mover o carrinho sobre o trilho.
* **pivot:** Uma junta contínua permitindo a rotação do pêndulo em torno do carrinho.

O pêndulo pode se mover livremente sem nenhuma entrada de controle direto e se mantém equilibrado através do movimento do carrinho. Quando o carrinho é empurrado para um lado, o pêndulo naturalmente se inclina na direção oposta. O arquivo [`cartpole.urdf.xacro`](https://raw.githubusercontent.com/fabiobento/cont-int-2026-1/refs/heads/main/modulo_simulacao_4/scripts/cartpole_description/urdf/cartpole.urdf.xacro) define as juntas e os elos para este sistema. Neste arquivo habilitamos o controle de esforço, que é refletido na seção `ros2_control` do arquivo *xacro*. A tag `ros2_control` é usada para definir como as juntas são controladas. Incluímos a interface de *hardware* para fazer a interface com as juntas simuladas.

```xml
    <!-- 
        Interface do ros2_control para o simulador Ignition (Gazebo Harmonic).
        Mapeia os comandos de atuação e sensores para que o ROS possa interagir com 
        os objetos descritos no mundo físico virtual.
    -->
    <ros2_control name="IgnitionSystem" type="system">
        <hardware>
            <!-- Carrega o plugin do sistema de controle via ros2 para o Gazebo Ignition -->
            <plugin>ign_ros2_control/IgnitionSystem</plugin>
        </hardware>

```

A junta linear é comandada usando uma entrada de controle de esforço. No entanto, estamos interessados em saber sua posição ao longo do trilho para posicioná-la no meio do trilho no início de um novo episódio de treinamento.

```xml
        <!-- Mapeamento da junta linear (do carrinho) -->
        <joint name="linear">
            <!--<command_interface name="position" />-->
            <!-- Habilita a escrita/comando por esforço dinâmico (Força Linear) -->
            <command_interface name="effort" />

            <!-- Interfaces de leitura de estado de sensores -->
            <state_interface name="position">
                <param name="initial_value">0.0</param>
            </state_interface>
            <state_interface name="velocity"/>
            <state_interface name="effort"/>
        </joint>

```

A mesma interface de controle é usada para a junta rotacional conectada ao pêndulo. Embora não precisemos de um controlador para esta junta (já que o objetivo é estabilizar o pêndulo indiretamente movendo o carrinho para a esquerda ou para a direita), o sistema deve iniciar com o pêndulo em uma posição estável, que é um ângulo de 0.0, conforme mostrado na Figura 2. Usando o controlador de esforço, o pêndulo ainda estará livre para se mover ao redor do carrinho durante a simulação.

```xml
        <!-- Mapeamento da junta pivot (do pêndulo) -->
        <joint name="pivot">
            <!-- Habilita a escrita/comando por esforço dinâmico (Torque Angular) -->
            <command_interface name="effort" />
            
            <!-- Interfaces de leitura de estado de sensores -->
            <state_interface name="position">
                <param name="initial_value">0.0</param>
            </state_interface>
            <state_interface name="velocity"/>
            <state_interface name="effort"/>
        </joint>
    </ros2_control>

```

Como de costume, devemos incluir o *plugin* onde os arquivos de configuração YAML do controlador especificam os tipos de controlador e as juntas envolvidas.

```xml
    <!-- 
        Plugin que atrela as configurações do hardware descrito à simulação do Gazebo.
        Injeta os parâmetros definidos no arquivo 'cartpole_controller.yaml' para que 
        o Broadcaster e os Controllers saibam o que ler e publicar.
    -->
    <gazebo>
        <plugin filename="ign_ros2_control-system" name="ign_ros2_control::IgnitionROS2ControlPlugin">
        <parameters>$(find cartpole_description)/config/cartpole_controller.yaml</parameters>
        </plugin>
    </gazebo>

```

Junto com o modelo do robô, devemos criar um arquivo *launch* para iniciar a simulação e os controladores de esforço para a base e para a haste do pêndulo. No pacote do repositório do GitHub, chamamos este arquivo de `cartpole.launch.py`. Após editar o `CMakeLists.txt` para instalar os diretórios `urdf` e `launch`, você pode iniciar a simulação usando os seguintes comandos:

```bash
$ colcon build --symlink-install
$ source install/setup.bash
$ ros2 launch cartpole_description cartpole.launch.py
```

Da simulação, usaremos os seguintes tópicos:

* `/effort_control/commands` : Para controlar o esforço da base para mover o carrinho.
* `/stick_effort_control/commands` : Para controlar a haste em torno do pêndulo na fase de *reset* (reinício).
* `/joint_states` : Para ler o estado do sistema, obtendo as observações dele.

Outro aspecto chave da simulação é que o modelo do robô deve ser fisicamente controlável. Isso depende muito dos parâmetros dinâmicos do modelo. Por exemplo, se o carrinho for muito leve e o pêndulo for muito pesado, será impossível controlar a orientação do pêndulo, mesmo com uma abordagem de DRL. Isso destaca a importância de ter um modelo de simulação preciso para um controle bem-sucedido.

Após obter um modelo de simulação correto, precisamos de uma função para reiniciar o estado do sistema: o carrinho no meio do trilho e o pêndulo perpendicular ao carrinho.

Por esse motivo, criaremos o pacote [`cartpole_reset`](https://github.com/fabiobento/cont-int-2026-1/tree/main/modulo_simulacao_4/scripts/cartpole_reset)(disponível [**nesse link**](https://github.com/fabiobento/cont-int-2026-1/tree/main/modulo_simulacao_4/scripts/cartpole_reset)) que recebe um sinal como entrada para reiniciar o estado da simulação.

```bash
$ ros2 pkg create --build-type ament_python cartpole_reset --dependencies rclpy std_msgs
```

Este pacote contém o nó [`cartpole_reset.py`](https://github.com/fabiobento/cont-int-2026-1/blob/main/modulo_simulacao_4/scripts/cartpole_reset/cartpole_reset/cartpole_reset.py). Seu conteúdo é discutido a seguir:

1. Primeiro, importamos os módulos Python necessários. O tipo de dados `Float64MultiArray` é usado para enviar comandos às juntas do controlador. Embora tenhamos uma junta por controlador, ainda precisamos preencher o *array* com um único elemento para cada junta.

```python
"""
Módulo ROS 2 responsável por redefinir e estabilizar o sistema do Cartpole.

Este script implementa um nó que monitora o estado das juntas e, ao receber um comando 
de reset, utiliza controladores Proporcionais-Derivativos (PD) independentes para retornar o carrinho à posição inicial e estabilizar o pêndulo na posição vertical.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray, Bool
from sensor_msgs.msg import JointState
from threading import Thread
import math
```

2. Precisamos de uma função adequada para reportar o ângulo do estado da junta dentro de um limite adequado. Conforme definido no modelo do robô, esse elo (*link*) é um elo contínuo; isso significa que, ao realizar múltiplas rotações, seu valor tende a um valor infinito. Diferentemente, precisamos que o ângulo seja delimitado no intervalo `-pi` a `pi`.

```python
# Função para garantir que o ângulo do pêndulo fique restrito entre -pi e pi
def bound_angle(angle):
    """
    Mantém o valor do ângulo delimitado no intervalo de -pi a pi radianos.

    Args:
        angle (float): Ângulo contínuo em radianos.

    Returns:
        float: O ângulo equivalente ajustado para o intervalo [-pi, pi].
    """
    bounded_angle = (angle + math.pi) % (2 * math.pi) - math.pi
    return bounded_angle
```

3. No construtor da classe, definiremos a entrada e a saída usando os dados do ROS 2.

```python
   def __init__(self):
        """
        Inicializa o nó, configurando as inscrições (subscriptions), publicadores
        (publishers) e o timer necessários para o controle das juntas do robô.
        """
        # Inicializa o nó (nomeado como 'yolo_node', embora controle o reset do cartpole)
        super().__init__('yolo_node')
        
        # Inscreve-se no tópico de estados das juntas para receber posições e velocidades
        self.js_sub = self.create_subscription(JointState, "/joint_states", self.js_cb, 10)
        
        # Publicadores de comandos de esforço (effort/torque) para o carrinho e para o pêndulo
        self.cartpole_eff_pub = self.create_publisher(Float64MultiArray, "/effort_control/commands", 10)
        self.system_ready_pub = self.create_publisher(Bool, "/cartpole/ready", 10)
        self.cartpole__reset_sub = self.create_subscription(Bool, "/cartpole/reset", self.reset, 10)
        self.stick_eff_pub = self.create_publisher(Float64MultiArray, "/stick_effort_control/commands", 10)
        
        # Publicador que indica se o sistema está pronto e inscrição para iniciar o reset
        self.system_ready_pub = self.create_publisher(Bool, "/cartpole/ready", 10)
        self.cartpole__reset_sub = self.create_subscription(Bool, "/cartpole/reset", self.reset_callback, 10)

```

4. Quando o carrinho está na posição de reinício, publicamos uma *flag* (bandeira) booleana para informar ao *software* de terceiros (o ambiente de treinamento neste caso) sobre o status do sistema. Se essa *flag* for verdadeira, o sistema está pronto; caso contrário, está no estado de *reset*.

```python
        # Timer para publicar repetidamente que o sistema está pronto
        self.timer = self.create_timer(0.1, self.publish_system_ready)
        
        # Flags e variáveis de controle interno
        self.reset = False
        self.js_ready = False
        self.js = None
        self.system_ready = Bool()
        self.system_ready.data = True

```

5. No *loop* principal, aguardamos uma nova solicitação de reinício do sistema. Naturalmente, devemos esperar até que o status do sistema esteja pronto, recebendo os estados das juntas. Essa verificação é executada em uma taxa baixa (2 Hz).

```python
    def main_loop(self): 
        """
        Loop de execução principal executado em uma thread separada.
        
        Este método aguarda um comando de reset e, em seguida, executa um 
        loop de controle a 100 Hz utilizando controladores PD para estabilizar 
        tanto a posição linear do carrinho quanto a posição angular do pêndulo.
        """
       
        rate = self.create_rate(2)
        
        # Aguarda até receber o primeiro dado de estado das juntas
        while not self.js_ready:
            rate.sleep()   
            
        # Loop principal enquanto o ROS estiver rodando
        while rclpy.ok():

            # Verifica se uma solicitação de reset foi recebida
            if( self.reset == True):

```

6. Quando uma requisição de reinício é recebida, configuramos as funções necessárias para colocar o sistema no estado de reinício. Por este motivo, implementamos dois controladores Proporcional-Derivativo (PD). Esses PDs obtêm os erros de posição a partir dos ângulos do carrinho e do pêndulo e geram um torque adequado para manter o sistema no estado de reinício.

- A equação geral de controle de um controlador PD é dada por:

$$u(t) = K_p \cdot e(t) + K_d \cdot \frac{de(t)}{dt}$$

- Onde:
  - $u(t)$ é o sinal de controle (força ou torque) aplicado ao sistema.
  - $e(t)$ é o erro atual (a diferença entre a posição/ângulo atual e a posição/ângulo desejado, que no caso do reset é zero).
  - $\frac{de(t)}{dt}$ é a derivada do erro (a taxa de variação do erro ao longo do tempo, ou seja, a velocidade com que o sistema está se afastando ou se aproximando do alvo).
  - $K_p$ é o ganho proporcional.
   - $K_d$ é o ganho derivativo.

- Essa equação geral se desdobra em **duas equações específicas** para o sistema Cart-Pole:

    - 1. **Equação do Carrinho (Controle Linear)**

        Esta equação calcula a força necessária para empurrar o carrinho de volta para o centro da pista (posição 0).

        $$F_{cart} = K_p^{cart} \cdot e_{cart} + K_d^{cart} \cdot \dot{e}_{cart}$$

        No código em Python, os termos correspondem a:

        * $K_p^{cart} \rightarrow$ `k = 0.8`
        * $K_d^{cart} \rightarrow$ `k2 = 0.2`
        * $e_{cart} \rightarrow$ `cart_e` (Erro de posição)
        * $\dot{e}_{cart} \rightarrow$ `cart_e_derivative` (Derivada do erro do carrinho)

    - 2. **Equação do Pêndulo (Controle Angular)**

        Esta equação calcula o torque (esforço) rotacional aplicado na junta contínua para levantar e manter a haste equilibrada perfeitamente na vertical (ângulo 0).

        $$\tau_{pole} = K_p^{pole} \cdot e_{pole} + K_d^{pole} \cdot \dot{e}_{pole}$$

        No código em Python, os termos correspondem a:

        * $K_p^{pole} \rightarrow$ `k_stick = 0.1`
        * $K_d^{pole} \rightarrow$ `k2_stick = 0.05`
        * $e_{pole} \rightarrow$ `stick_e` (Erro angular da haste)
        * $\dot{e}_{pole} \rightarrow$ `stick_derivative` (Derivada do erro da haste)

- Para forçar o robô de volta à sua posição inicial de forma estável, o nó de *reset* implementa duas equações de controle Proporcional-Derivativo (PD).A força linear do carrinho ($F$) e o torque angular da haste ($\tau$) são calculados através das seguintes equações:

$$F = (k \cdot e_{cart}) + (k2 \cdot \dot{e}_{cart})$$
$$\tau = (k_{stick} \cdot e_{stick}) + (k2_{stick} \cdot \dot{e}_{stick})$$

- Onde $e$ representa o erro de posição (o quão longe o robô está do centro absoluto) e $\dot{e}$ representa a derivada desse erro (a velocidade do movimento). Os ganhos do código (`k=0.8`, `k2=0.2`, `k_stick=0.1`, `k2_stick=0.05`) atuam como multiplicadores, calibrando a intensidade com que o simulador vai puxar as juntas do robô de volta para a origem (0.0).

```python
                # Publica que o sistema não está pronto durante o procedimento de reset
                self.system_ready.data = False
                self.system_ready_pub.publish(self.system_ready)
              
                # Taxa de controle interno de 100 Hz
                rate2 = self.create_rate(100)
                
                # Reseta a flag para evitar múltiplos resets simultâneos
                self.reset = False
         
                # Mensagens de comando
                cmd = Float64MultiArray()  
                stick_tau_cmd = Float64MultiArray()                
              
                # Ganhos PD para o controle do carrinho (linear)
                k = 0.8
                k2 = 0.2
                
                # Ganhos PD para o controle do pêndulo (angular)
                k_stick = 0.1
                k2_stick = 0.05
                
                # Variáveis de erro do pêndulo
                stick_e = 0.0
                prev_stick_e = 0.0
                stick_derivative = 0.0
                
                # Variáveis de erro do carrinho
                cart_e = 0 
                prev_cart_e = 0
                cart_e_derivative = 0

```

7. Os erros iniciais no carrinho e no pêndulo são obtidos dos estados das juntas, e o *loop* de controle principal do nó começa. A ação de controle continua até que as condições de reinício sejam atendidas — especificamente, quando o pêndulo estiver na posição de reinício e sua velocidade for quase zero. E quanto à posição do carrinho no trilho? Não definimos isso explicitamente, pois não estamos focados em ter o carrinho exatamente na posição 0.0. No entanto, se o carrinho se mover muito em direção ao centro do trilho, isso fará com que o pêndulo se mova, dificultando sua estabilização e aumentando sua velocidade. Embora o carrinho não precise estar perfeitamente no 0, nosso objetivo é mantê-lo mais perto do centro.

    Neste trecho, o algoritmo define as **condições de tolerância** para considerar o sistema estabilizado e calcula a **derivada numérica** do erro em tempo real.

    - **1. Condição de Estabilização (Loop *While*)**
    O controle PD de reinício não exige perfeição matemática absoluta (o que seria impossível no mundo físico simulado), mas sim que o sistema entre em uma zona de tolerância aceitável. O laço de controle continua atuando *enquanto* a inclinação do pêndulo ou a velocidade do carrinho forem significativas:

    $$|\theta(t)| > 0.05 \quad \lor \quad |\dot{x}(t)| > 0.01$$

    Onde:
    * $|\theta(t)|$ corresponde a `math.fabs(stick_js)`, o valor absoluto do ângulo da haste (tolerância de $\approx 2.86^\circ$).
    * $|\dot{x}(t)|$ corresponde a `math.fabs(self.js.velocity[0])`, o valor absoluto da velocidade do carrinho (tolerância de $1$ cm/s).
    * O símbolo $\lor$ (OU) indica que se *qualquer uma* das duas condições for violada, o robô ainda não está pronto.

    - **2. Cálculo do Erro de Posição**
    Como o objetivo é trazer o carrinho de volta para a origem (ponto $0.0$ do trilho), o erro de posição $e_{cart}(t)$ em qualquer instante de tempo é simplesmente a sua posição atual menos o alvo:

    $$e_{cart}(t) = x(t) - 0 \implies e_{cart}(t) = x(t)$$
    *(No código: `cart_e = self.js.position[0]`)*

    - **3. Derivada Numérica do Erro (Diferença Finita)**
    Para o termo derivativo do controlador PD ($K_d$), o nó precisa saber a taxa de variação do erro (velocidade). Como estamos operando em um sistema discreto controlado por software, calculamos isso usando a **Aproximação de Euler (Diferença Finita para trás)**:

    $$\dot{e}_{cart}(t) \approx \frac{e_{cart}(t) - e_{cart}(t - \Delta t)}{\Delta t}$$

    Onde:
    * $e_{cart}(t)$ é o erro no ciclo atual (`cart_e`).
    * $e_{cart}(t - \Delta t)$ é o erro do ciclo anterior (`prev_cart_e`).
    * $\Delta t$ é o intervalo de tempo entre as execuções. Como definimos que o controle roda a 100 Hz (`rate2 = self.create_rate(100)`), o $\Delta t$ é de $\frac{1}{100}$ de segundo.

    *(No código, isso é implementado literalmente como: `cart_e_derivative = (cart_e - prev_cart_e) / (1.0/100.0)`)*

```python
                # Obtendo posições iniciais
                cart_e = self.js.position[0]
                prev_cart_e = 0
                
                stick_js = bound_angle(self.js.position[1])
                
                # Enquanto o pêndulo estiver inclinado ou a velocidade do carrinho não for zero
                while ( (math.fabs( stick_js) > 0.05) or (math.fabs(self.js.velocity[0]) > 0.01) ) :
                     
                    # Controle PD do carrinho (aproximando da posição 0)
                    cart_e = (self.js.position[0])
                    cart_e_derivative = (cart_e - prev_cart_e) / (1.0/100.0)

```

8. O esforço tanto para o carrinho quanto para o pêndulo é calculado usando a fórmula do controlador PD, que combina um ganho aplicado ao erro atual (a diferença entre a posição atual e a desejada) e outro ganho aplicado à derivada do erro (a taxa de variação do erro). Antes de enviar o comando de esforço, também precisamos determinar se um torque positivo ou negativo é necessário para mover o modelo simulado para a posição desejada.

```python
                   cart_c = k*cart_e + k2*cart_e_derivative
                    cmd.data = [-cart_c]

                    # Controle PD do pêndulo (aproximando do ângulo 0)
                    stick_js = bound_angle(self.js.position[1])
                    
                    stick_e = math.fabs( stick_js )
                    stick_derivative = (stick_e - prev_stick_e) / (1.0/100.0)

                    tau = k_stick*stick_e + k2_stick*stick_derivative

                    # Ajusta a direção do torque dependendo de qual lado o pêndulo caiu
                    if ( stick_js > 0 ):
                        tau = -tau
                    
                    stick_tau_cmd.data = [tau]
                    
                    # Publica os torques / forças calculadas
                    self.cartpole_eff_pub.publish(cmd)
                    self.stick_eff_pub.publish(stick_tau_cmd)
                    
                    # Atualiza os estados anteriores
                    prev_stick_e = stick_e
                    prev_cart_e = cart_e

                    # Dorme para manter a frequência de 100 Hz
                    rate2.sleep()

```

9. O restante do código contém as funções para receber como entrada a solicitação de reinício, os estados das juntas e a *thread* para publicar quando a função de reinício for concluída.

```python
    def reset_callback(self, msg):
        """
        Callback acionado ao receber uma mensagem no tópico de reset.
        """
    def reset(self, msg):
        self.reset = True

    # Função para publicar periodicamente que o sistema está pronto (ready)
    def publish_system_ready(self):
        """
        Publica repetidamente o status atual do sistema no tópico respectivo.
        """
        self.system_ready_pub.publish(self.system_ready)

    # Callback para atualizar os dados mais recentes das juntas
    def js_cb(self, msg):
        """
        Callback que atualiza a variável local de estados das juntas.

        Args:
            msg (sensor_msgs.msg.JointState): Mensagem contendo o estado atual das juntas.
        """
        self.js = msg
        self.js_ready = True

    # Inicia a thread separada para o loop de controle e permite que o nó receba mensagens
    def run( self ):
        """
        Inicia a execução do nó. 
        
        Cria uma thread paralela para executar o 'main_loop', garantindo que
        o spin do ROS 2 não seja bloqueado e as mensagens continuem sendo processadas.
        """
        main_loop_thread = Thread(target = self.main_loop, args = ())
        main_loop_thread.start()
        rclpy.spin(self)

def main(args=None):
    """
    Função principal de entrada do script. Inicializa a comunicação ROS 2 
    e coloca o nó em execução.
    """
    rclpy.init(args=args)

    node = CartPoleReset()
    node.run()

if __name__ == '__main__':
    main()

```

Precisamos adicionar este nó ao arquivo de configuração [`setup.py`](https://github.com/fabiobento/cont-int-2026-1/blob/main/modulo_simulacao_4/scripts/cartpole_reset/setup.py) e compilar o *workspace*.

Agora temos todos os elementos para integrar o Gymnasium com o ROS 2 e criar nosso primeiro ambiente.

## **Integrando o Gymnasium e o ROS 2**

Para integrar o [Gymnasium](https://gymnasium.farama.org/index.html) com o ROS 2, precisamos implementar suas funções principais usando a API do ROS 2 para controlar a simulação. Isso nos permite usar a mesma interface de controle durante o teste do sistema, de modo que, se tivermos um sistema físico idêntico, possamos aplicar perfeitamente o que o agente aprendeu no ambiente simulado ao sistema do mundo real.

Vamos criar o pacote [`cartpole_drl_ppo`](https://github.com/fabiobento/cont-int-2026-1/tree/main/modulo_simulacao_4/scripts/cartpole_drl_ppo) (disponível [**nesse link**](https://github.com/fabiobento/cont-int-2026-1/tree/main/modulo_simulacao_4/scripts/cartpole_drl_ppo)) no ROS 2 contendo
- o ambiente,
- o treinamento do modelo
- e o uso na fase de execução.

```bash
$ ros2 pkg create cartpole_drl_ppo --build-type ament_python --dependencies rclpy std_msgs sensor_msgs geometry_msgs
```

Neste pacote, implementaremos os seguintes *scripts*:

* [`cartpole_env.py`](https://github.com/fabiobento/cont-int-2026-1/blob/main/modulo_simulacao_4/scripts/cartpole_drl_ppo/cartpole_drl_ppo/cartpole_env.py) : Implementa o ambiente Gymnasium usado tanto no treinamento quanto no uso.
* [`cartpole_training.py`](https://github.com/fabiobento/cont-int-2026-1/blob/main/modulo_simulacao_4/scripts/cartpole_drl_ppo/cartpole_drl_ppo/cartpole_training.py) : O nó que usa o ambiente para realizar o treinamento do sistema.
* [`cartpole_prediction.py`](https://github.com/fabiobento/cont-int-2026-1/blob/main/modulo_simulacao_4/scripts/cartpole_drl_ppo/cartpole_drl_ppo/cartpole_prediction.py) : O nó que usa o modelo treinado para calcular a próxima ação para realizar a tarefa.

Vamos começar discutindo o script [`cartpole_env.py`](https://github.com/fabiobento/cont-int-2026-1/blob/main/modulo_simulacao_4/scripts/cartpole_drl_ppo/cartpole_drl_ppo/cartpole_env.py). Para otimizar a discussão, mostraremos apenas algumas partes mais relevantes do *script*. Como de costume, verifique o [repositório de código-fonte](https://github.com/fabiobento/cont-int-2026-1/blob/main/modulo_simulacao_4/scripts/cartpole_drl_ppo/cartpole_drl_ppo/cartpole_env.py) para a sua versão completa.

1. No início, junto com as dependências do ROS 2, importamos os módulos para usar o *gymnasium*. Isto é, o *gymnasium* em geral e o espaço (*space*) do Gymnasium.

```python
"""
Ambiente Customizado Gymnasium para o Pêndulo Invertido (CartPole) com ROS 2 e Gazebo.

Este módulo implementa a classe de ambiente que atua como ponte entre a 
biblioteca de Aprendizado por Reforço (como Stable Baselines3) e o simulador 
físico (Ignition/Harmonic Gazebo) gerenciado pelo ROS 2.
"""

import rclpy
import gymnasium as gym
from gymnasium import spaces
import numpy as np
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import Bool
from threading import Thread
import threading
import time
import math

```

2. A classe principal herda da classe *Environment* (Ambiente) do Gymnasium. Isso dá acesso ao mecanismo interno do Gymnasium para realizar o treinamento do sistema.

```python
class CartPoleROS2Env(gym.Env):
    """
    Ambiente Gymnasium integrado com ROS 2 para controle do CartPole.

    Esta classe empacota a comunicação assíncrona do ROS 2 (tópicos e callbacks)
    no padrão síncrono de passos (steps) esperado pelos algoritmos de DRL.

    Atributos:
        action_space (gymnasium.spaces.Box): Espaço contínuo de ações definindo a força.
        observation_space (gymnasium.spaces.Box): Espaço contínuo do estado do robô.
        node (rclpy.node.Node): Nó embutido do ROS 2 para comunicação.
    """
    
    def __init__(self):
        """
        Inicializa o espaço de ação, espaço de observação e a comunicação ROS 2.
        """
        super(CartPoleROS2Env, self).__init__()

```

3. Vamos definir o espaço de ação (*action space*), que especifica as possíveis ações que o robô pode tomar de forma discreta ou contínua a cada iteração. No nosso caso, temos duas ações básicas: aplicar uma força para empurrar o carrinho para a esquerda ou para a direita. No entanto, como queremos modular continuamente a força (por exemplo, aplicando mais força quando a haste está caindo), definimos o espaço de ação como um intervalo contínuo de valores de -15 N a 15 N (aproximadamente 1,5 kg de força).

```python
        # Define o espaço de ações: um valor contínuo (esforço/força em Newtons)
        # Os limites definidos são de -15.0 N a 15.0 N para a base prismática.
        self.action_space = spaces.Box(low=-15.0, high=15.0, shape=(1,), dtype=np.float32)


```

4. Também precisamos definir o espaço de observação (*observation space*), que inclui o conjunto de valores possíveis que representam o estado do robô. Isso incluirá a posição do carrinho no trilho, sua velocidade, bem como a posição e a velocidade da haste. Devemos definir limites apropriados para esses valores para garantir que o espaço de observação permaneça dentro de limites adequados.

```python
        # Limites para o espaço de observações:
        # [posição_carro (m), velocidade_carro (m/s), ângulo_haste (rad), velocidade_angular_haste (rad/s)]
        high = np.array([5.0, 1.0, math.pi, 8.5], dtype=np.float32)
        self.observation_space = spaces.Box(-high, high, dtype=np.float32)

```

5. Agora podemos inicializar o nó ROS 2 para fazer a interface com a rede ROS 2. Neste contexto, o nó é inicializado sem argumentos. Após a inicialização, a saída (o comando de esforço do *cart-pole*) e a entrada (o espaço observado, recebido através de `joint_states`) são vinculados. Os tópicos para solicitar um novo reinício (*reset*) do sistema e receber o estado de prontidão (*readiness*) do simulador são recebidos.

```python
        # Inicialização do nó interno do ROS 2
        rclpy.init(args=None)
        self.node = rclpy.create_node('cartpole_gym_env')
        
        # Configuração dos Publishers (Comandos) e Subscribers (Sensores e Status)
        self.cartpole_eff_pub = self.node.create_publisher(Float64MultiArray, "/effort_control/commands", 10)
        self.joint_state_sub = self.node.create_subscription(JointState, '/joint_states', self.joint_state_callback, 10 )
        self.cartpole_reset_pub = self.node.create_publisher(Bool, "/cartpole/reset", 10)
        self.system_ready_sub = self.node.create_subscription(Bool, '/cartpole/ready', self.system_ready_cb, 10 )

        # Inicialização das variáveis de estado interno
        self.current_observation = np.zeros(4, dtype=np.float32)
        self.state_received = False
        self.system_ready = False

```

6. Para permitir que o ROS 2 opere corretamente, nós o executamos em segundo plano usando um `SingleThreadedExecutor`, que gerencia os *callbacks* do nó. Uma *thread* separada é criada para executar continuamente a função `spin()` do nó, permitindo que o nó lide com mensagens e eventos de forma assíncrona enquanto o programa principal é executado.

```python
        # Configura um executor do ROS 2 em uma thread separada em background.
        # Isso permite que os callbacks de sensores continuem atualizando os 
        # dados assincronamente enquanto o algoritmo de IA realiza os cálculos.
        self.executor = rclpy.executors.SingleThreadedExecutor()
        self.executor.add_node(self.node)
        self.spin_thread = threading.Thread(target=self.executor.spin, daemon=True)
        self.spin_thread.start()

```

7. No `joint_state_callback`, preenchemos os dados de observação. Como já dito, isso representa o estado do agente, nos dando uma recompensa positiva ou negativa. Além disso, neste caso, como no nó de *reset*, devemos limitar o ângulo da haste, fazendo com que fique dentro do intervalo adequado `-pi`, `pi`.

```python

    def joint_state_callback(self, msg):
        """
        Callback de leitura dos encoders (sensores de junta) do simulador Gazebo.

        Atualiza o vetor de observação da IA sempre que o ROS 2 publica novos dados.

        Argumentos:
            msg (sensor_msgs.msg.JointState): Mensagem contendo posição e velocidade atual.
        """
        try:
            # Constrói o vetor de observação processando a cinemática básica
            self.current_observation = np.array([
                msg.position[0],               # Posição linear do carrinho
                msg.velocity[0],               # Velocidade linear do carrinho
                bound_angle(msg.position[1]),  # Ângulo normalizado da haste
                msg.velocity[1]                # Velocidade angular da haste
            ], dtype=np.float32)
            
            self.state_received = True
        except ValueError:
            # Ignora falhas de leitura temporárias antes dos controladores inicializarem completamente
            pass

```

8. Vamos agora discutir a função `step`. Lembre-se que esta função é chamada a cada iteração, realizando uma ação e avaliando as observações para entender se a ação dá ao robô uma recompensa positiva ou leva ao término do episódio. Por este motivo, esta função é executada apenas se o estado do agente estiver disponível.

```python
    def step(self, action):
        """
        Aplica a força calculada pela IA ao robô e avança um passo no tempo.

        Argumentos:
            action (numpy.ndarray): O vetor de ação gerado pela política do agente (esforço).

        Retorna:
            tuple: Contendo:
                - obs (numpy.ndarray): O novo estado após aplicar a ação.
                - reward (float): A recompensa obtida neste passo de tempo.
                - done (bool): Verdadeiro se o episódio falhou (queda) e precisa terminar.
                - truncated (bool): Verdadeiro se o tempo limite do episódio foi atingido.
                - info (dict): Dicionário de informações adicionais (vazio por padrão).
        """
        # Trava de segurança: Aguarda o primeiro dado de sensor antes de agir
        if not self.state_received:
            time.sleep(0.01)
            return self.current_observation, 0.0, False, False, {}

```

9. Uma vez que a ação gerada pelo agente para tentar realizar a tarefa é diretamente a força aplicada ao carrinho, nós publicamos seu valor no tópico de comando de controle de esforço, e então esperamos que a malha de controle da simulação do *ros2_control* (100 Hz) avalie as observações.

```python
        # Empacota o esforço gerado pela Rede Neural e envia para o ROS 2 Control
        eff_msg = Float64MultiArray()
        eff_msg.data = [float(action[0])]
        self.cartpole_eff_pub.publish(eff_msg)
        
        # Aguarda a física do Gazebo processar a força (simulando a taxa de 100Hz de controle)
        time.sleep(0.01)  
        
        obs = self.current_observation.copy()
        reward = 1.0  # Recompensa padrão por manter o pêndulo em pé neste instante

```

10. O episódio de aprendizado é considerado encerrado se alguma das seguintes condições for atendida: a posição do carrinho for além de `[-2, 2]` metros, o ângulo da haste exceder `[π/4, -π/4]` radianos (`obs[0]` e `obs[2]`, respectivamente), a velocidade rotacional da haste for maior que `0.3` rad/s, ou a velocidade do carrinho exceder `1` m/s. Se alguma dessas observações cair fora da faixa aceitável, será impossível estabilizar a haste e impedi-la de oscilar.

```python
        # Condições de falha (Término do Episódio):
        # 1. Carro saiu da pista útil (-2m a 2m)
        # 2. Haste inclinou mais que 45 graus (pi/4)
        # 3. Velocidade angular excessiva (instabilidade iminente)
        # 4. Velocidade linear excessiva (risco de bater no fim do trilho)
        done = bool(
            obs[0] < -2 or obs[0] > 2 or
            obs[2] < -math.pi/4 or obs[2] > math.pi/4 or 
            math.fabs( obs[3] > 0.3 ) or 
            math.fabs( obs[1] > 1.0 )
        )
```

11. A cada iteração, o sistema fornece `1` ponto de recompensa se a haste estiver estável no carrinho (todas as condições do estado são válidas). Caso contrário, nenhuma recompensa é fornecida. Adicionalmente, queremos ter certeza de que a velocidade do carrinho seja a mais suave possível. Quando sua velocidade aumenta, a estabilidade da haste é difícil de manter. Por esta razão, fornecemos uma recompensa negativa se sua velocidade for maior do que o esperado.

```python
        # Modulação de Recompensa (Shaping): Penaliza severamente comportamentos oscilatórios
        # ou violentos do carrinho para forçar um aprendizado mais suave e seguro.
        if( math.fabs( obs[1] > 1.0 ) ): 
           reward = -10
        
        truncated = False
        info = {}

```

12. Por fim, retornamos o conjunto de dados recuperados deste episódio. Além disso, podemos considerar uma condição de truncamento (*truncation condition*). Isso acontece quando o episódio termina precocemente devido a limites de tempo ou condições externas. No nosso caso, isso nunca acontecerá.

```python
        return obs, reward, done, truncated, info

```

13. A função `reset` é outra parte fundamental do ambiente. Ela envia um sinal de reinício para acionar o processo de *reset* no nó de reinício e aguarda a confirmação de que o sistema está de volta ao estado pronto. O nó de *reset* nos notifica quando o sistema estiver pronto.

```python
    def reset(self, seed=None, options=None):
        """
        Reinicia fisicamente o ambiente para iniciar um novo episódio de treinamento.

        Esta função se comunica com o nó auxiliar `cartpole_reset` para aplicar
        os PIDs virtuais que levantam o pêndulo de volta à posição inicial no simulador.

        Argumentos:
            seed (int, opcional): Semente de aleatoriedade para reprodutibilidade.
            options (dict, opcional): Opções extras de reset.

        Retorna:
            tuple: Contendo a observação inicial após o reset e o dicionário de informações.
        """
        if seed is not None:
             np.random.seed(seed)
            
        # Dispara o comando de reset pela rede do laboratório
        reset_data = Bool()
        reset_data.data = True
        self.cartpole_reset_pub.publish( reset_data )
        time.sleep(0.5) # Tempo de tolerância para o nó de reset assumir o controle

        # Bloqueia o avanço da Inteligência Artificial até que o braço invisível 
        # (nó de reset) confirme que posicionou o pêndulo no centro e parou de tremer.
        while( not self.system_ready ):
            time.sleep(0.001)

        info = {}
        return self.current_observation.copy(), info

```

14. Finalmente, na função `close`, devemos apenas sair de forma limpa do nó ROS 2.

```python
        """
        Desliga ordenadamente o ambiente, encerrando as threads em background e
        fechando o nó do ROS 2 para liberar os recursos do sistema operacional.
        """
        self.executor.shutdown()
        self.node.destroy_node()
        rclpy.shutdown()

```

Concluímos agora nosso primeiro ambiente Gymnasium. Isso significa que podemos escrever o procedimento para treinar o agente neste ambiente e com os dados de simulação do Gazebo, conforme discutido nas próximas seções.

### **Treinando um Robô Usando o Gymnasium e stable_baselines3**

Escrever um ambiente Gymnasium adequado é apenas um passo básico para treinar nosso robô. O próximo passo é fazer o robô interagir com o ambiente, selecionando adequadamente as ações a serem executadas, coletando as recompensas e treinando a rede neural profunda. Essa rede neural é quem direciona as ações do robô na fase de predição, quando o robô finalmente for capaz de realizar as ações por conta própria. Para simplificar a etapa de treinamento, usaremos outra biblioteca, tipicamente conectada com o Gymnasium, que é a [**Stable-Baselines3**](https://stable-baselines3.readthedocs.io/en/master/) (SB3). Trata-se de uma biblioteca Python que fornece implementações de algoritmos de aprendizado por reforço (RL) no estado da arte. Alguns dos algoritmos de DRL mais difundidos implementados na SB3 são a Otimização de Política Proximal (PPO), *Deep Q-Network* (DQN) e *Soft Actor-Critic* (SAC). A SB3 é construída sobre o [PyTorch](https://pytorch.org/docs/stable/index.html) e pode ser usada diretamente em nossos nós Python do ROS 2.

**Nota:** O PyTorch é um popular *framework* de aprendizado profundo de código aberto conhecido por sua flexibilidade, gráficos de computação dinâmica e forte suporte a GPU. É amplamente utilizado para treinamento e experimentação de redes neurais em tarefas de IA.

Certifique-se de seu sistema tenha os seguinte resquisitos atendidos: `stable_baselines3`, `'numpy<2'` e `stable-baselines3[extra]`.

Adicione o nó  [`cartpole_training`](https://github.com/fabiobento/cont-int-2026-1/blob/main/modulo_simulacao_4/scripts/cartpole_drl_ppo/cartpole_drl_ppo/cartpole_training.py)   para realizar a fase de treinamento no mesmo pacote do ambiente `cartpole_drl_ppo`.

O conteúdo deste script é explicado a seguir:

1. No início, importamos o ambiente criado até agora. Adicionalmente, incluímos o módulo para realizar o método de treinamento de DRL desejado, o PPO (isto também motiva o nome do pacote). PPO significa *Proximal Policy Optimization* (Otimização de Política Proximal) e melhora os métodos de gradiente de política equilibrando exploração e estabilidade. Além disso, permite especificar um espaço de ação contínuo, diferentemente do conhecido *Deep Q-Network* (DQN), que só permite um espaço discreto. Por fim, queremos salvar o modelo diretamente no diretório de instalação do pacote. Por esse motivo, usamos o módulo `get_package_share_directory` de `ament_index_python.packages`.

```python
"""
Script de Treinamento do Agente de DRL (Deep Reinforcement Learning).

Este script inicializa o ambiente customizado CartPoleROS2Env e utiliza 
o algoritmo PPO (Proximal Policy Optimization) da biblioteca Stable Baselines3 
para treinar uma rede neural (MlpPolicy) a equilibrar o pêndulo.
Após o treinamento, o modelo resultante é salvo no diretório de instalação do pacote.
"""

from cartpole_drl_ppo.cartpole_env import CartPoleROS2Env
from stable_baselines3 import PPO
from ament_index_python.packages import get_package_share_directory

```

2. Na função principal, obtemos a pasta de instalação do pacote `cartpole_drl_ppo` para podermos salvar o arquivo do modelo treinado lá. Isso nos permite carregar o modelo facilmente mais tarde, quando precisarmos usá-lo para previsões.

```python
def main(args=None):
    """
    Função principal que orquestra a criação do ambiente, configuração e 
    execução do treinamento do modelo PPO.
    """
    package_name = 'cartpole_drl_ppo'
    # Obtém o caminho de instalação do pacote (onde o modelo será salvo)
    model_pkg_path = get_package_share_directory(package_name) + "/" 

```

3. Este código inicializa um modelo PPO com uma política de rede neural (`MlpPolicy`) para interagir com o ambiente (`env`). A opção `verbose=1` fornece registro detalhado durante o treinamento. Ela prepara o agente para aprender usando o algoritmo PPO no ambiente determinado. Após a inicialização do modelo, nós o treinamos. Treinamos o modelo por 15.000 *timesteps* (passos de tempo), o que significa que o agente interagirá com o ambiente esse número de vezes. A opção `progress_bar=True` mostra uma barra de progresso para acompanhar o processo de treinamento.

```python
    # Instancia o ambiente customizado do CartPole integrado com ROS 2
    env = CartPoleROS2Env()
    
    # Inicializa o modelo PPO utilizando uma política Multi-Layer Perceptron (MlpPolicy).
    # O device='cpu' é utilizado para remover o aviso do PyTorch e frequentemente melhora a 
    # velocidade para redes pequenas em comparação à transferência de dados para a GPU.
    model = PPO('MlpPolicy', env, verbose=1, device='cpu')

    # Inicia o processo de aprendizado (treinamento) do agente interagindo com o ambiente.
    # O total_timesteps define quantos passos (interações) o agente fará no total.
    # Exemplo: 500.000 passos garantem um bom tempo de exploração e consolidação da política.
    # A barra de progresso (progress_bar=True) facilita o acompanhamento no terminal.
    model.learn(total_timesteps=500000, progress_bar=True)

```

4. Finalmente, podemos salvar o modelo e fechar o ambiente.

```python
    # Salva os pesos e configurações da rede neural treinada no caminho do pacote
    model.save(model_pkg_path + "ppo_cartpole_ros2")

    # Encerra o ambiente corretamente após a conclusão do treinamento
    env.close()

```

Após modificar adequadamente o arquivo [`setup.py`](https://github.com/fabiobento/cont-int-2026-1/blob/main/modulo_simulacao_4/scripts/cartpole_drl_ppo/setup.py), compilar e carregar (*sourcing*) o *workspace*, podemos agora iniciar o processo de treinamento. Obviamente, antes de iniciá-lo, devemos lançar a simulação, o nó de *reset* e, finalmente, o processo de treinamento.

```bash
$ ros2 launch cartpole_description cartpole.launch.py
$ ros2 run cartpole_reset cartpole_reset
$ ros2 run cartpole_drl_ppo cartpole_training
```

Neste ponto, o robô começa a realizar diferentes tentativas para melhorar sua experiência no ambiente Gymnasium. O tempo necessário para concluir o processo depende da velocidade com que o robô aprende e do número de passos de tempo que definimos na função de aprendizado. No entanto, no terminal onde iniciamos o processo de treinamento, você pode acompanhar o processo de aprendizado. Um exemplo dessa saída é mostrado na Figura 3, e é explicado a seguir.

<a id="figure-3"></a>
![](https://raw.githubusercontent.com/fabiobento/cont-int-2026-1/main/modulo_simulacao_4/imagens/learning.png)
**Figura 3 - Atualização do processo de aprendizado.** 

A saída mostrada na Figura 3 fornece estatísticas-chave do processo de treinamento do PPO em um ponto específico. Em particular:

1. **Seção rollout/ (Desdobramento):**
* **`ep_len_mean` (169):** O comprimento médio do episódio, o que significa que os episódios do agente (do início ao fim) duram em média 169 passos.
* **`ep_rew_mean` (169):** A recompensa média por episódio, mostrando o desempenho do agente, sendo 169 a recompensa total média obtida em cada episódio.


2. **Seção time/ (Tempo):**
* **`fps` (28):** O número de quadros por segundo sendo processados durante o treinamento, indicando a velocidade de interação com o ambiente.
* **`iterations` (1):** O número de vezes que o modelo PPO foi atualizado até agora. Aqui, apenas uma iteração foi concluída.
* **`time_elapsed` (71):** O tempo total decorrido desde o início do treinamento, em segundos (71 segundos aqui).
* **`total_timesteps` (2048):** O número cumulativo de passos de tempo (*timesteps* - ações tomadas no ambiente) até agora no treinamento, que é 2048 neste ponto.


Após completar todos os passos de tempo, o modelo é salvo no diretório do pacote de instalação. Obviamente, ele só tem um bom desempenho se o processo de treinamento for concluído com sucesso. Vamos tentar usar este modelo no exemplo discutido na próxima seção.

### **Controlando um Robô Usando Aprendizado por Reforço Profundo**

Agora estamos prontos para usar o modelo para controlar o robô. Podemos adicionar um novo *script* Python chamado [`cartpole_prediction.py`](https://github.com/fabiobento/cont-int-2026-1/blob/main/modulo_simulacao_4/scripts/cartpole_drl_ppo/cartpole_drl_ppo/cartpole_prediction.py). O conteúdo é descrito a seguir:

1. As mesmas bibliotecas usadas no treinamento são usadas na fase de predição. Da mesma forma, carregamos o modelo considerando o que foi gerado no exemplo anterior.

```python
"""
Script de Inferência/Predição do Agente de DRL.

Este script carrega o modelo PPO previamente treinado e o utiliza para 
controlar o ambiente CartPoleROS2Env em tempo real. O robô tenta 
equilibrar o pêndulo infinitamente, reiniciando o episódio de forma 
automática sempre que o pêndulo cair ou o carrinho sair dos limites.
"""

import time
from stable_baselines3 import PPO
from cartpole_drl_ppo.cartpole_env import CartPoleROS2Env
from ament_index_python.packages import get_package_share_directory

def main(args=None):
    """
    Função principal que carrega o modelo treinado, inicializa o ambiente
    e executa o laço de controle (inferência) de forma contínua.
    """
    package_name = 'cartpole_drl_ppo'
    # Obtém o diretório de instalação do pacote onde o modelo foi salvo
    model_pkg_path = get_package_share_directory(package_name) + "/" 

    # Carrega a rede neural pré-treinada a partir do arquivo .zip.
    # Utilizamos device='cpu' para carregar o modelo sem gerar gargalos ou avisos
    # caso estejamos em uma máquina sem GPU ou com configurações PyTorch simples.
    model = PPO.load(model_pkg_path + "ppo_cartpole_ros2.zip", device='cpu')
    
    # Instancia o ambiente customizado integrado com ROS 2
    env = CartPoleROS2Env()
    
    print("Iniciando a Inteligência Artificial! Pressione Ctrl+C para parar.")

    try:
        # Laço infinito para o robô continuar tentando indefinidamente
        while True:
            # Reseta o ambiente para a posição inicial e obtém a primeira observação
            obs, _ = env.reset()
            # Tempo de espera para a física do simulador Gazebo estabilizar após o reset
            time.sleep(1) 

```

2. Começamos a execução e continuamos até que o sistema atenda à condição desejada: a haste (pêndulo) permanece equilibrada e o carrinho continua próximo ao centro do trilho. As ações geradas e executadas estão alinhadas com o que o agente aprendeu durante o treinamento.

```python
            done = False
            truncated = False
            
            # Laço do episódio atual: executa ações continuamente enquanto a simulação for válida
            # O laço para se o robô cair/sair da pista (done) ou o limite de tempo estourar (truncated)
            while not (done or truncated):        
                # A rede neural prevê a melhor ação a tomar com base na observação atual (obs)
                action, _ = model.predict(obs)
                
                # O ambiente aplica a ação e devolve o novo estado, a recompensa e os status
                obs, reward, done, truncated, info = env.step(action)
                
                # Pequena pausa para sincronizar os cálculos com o tempo de simulação
                time.sleep(0.01)
                
            # Mensagem exibida no terminal quando a condição "done" ou "truncated" for atingida
            print("O robô desequilibrou ou falhou! Reiniciando o episódio...")
            
    except KeyboardInterrupt:
        # Tratamento seguro caso o usuário decida parar a execução usando Ctrl+C no terminal
        print("Inferência encerrada pelo usuário (Ctrl+C).")
    finally:
        # Garante que as conexões do ROS 2 e threads sejam limpas antes de fechar o script
        env.close()

if __name__ == '__main__':
    main()

```

Se o treinamento for concluído com sucesso, ele pode rodar por várias horas sem desequilibrar a haste. Obviamente, antes de executá-lo, devemos modificar o arquivo ]`setup.py`](https://github.com/fabiobento/cont-int-2026-1/blob/main/modulo_simulacao_4/scripts/cartpole_drl_ppo/setup.py). A lista final dos pontos de entrada (*entry points*) é a seguinte:

```python
entry_points={
    'console_scripts': [
        'cartpole_training = cartpole_drl_ppo.cartpole_training:main',
        'cartpole_prediction = cartpole_drl_ppo.cartpole_prediction:main',
        'plot_data = cartpole_drl_ppo.plot_data:main'
    ],
},

```

Compile o *workspace*, carregue-o (*source*) e execute a predição usando os seguintes comandos:

```bash
$ ros2 launch cartpole_description cartpole.launch.py
$ ros2 run cartpole_reset cartpole_reset
$ ros2 run cartpole_drl_ppo cartpole_prediction

```

Os resultados da tarefa são mostrados na Figura 4, que exibe a posição e a velocidade do carrinho, bem como o ângulo e a velocidade angular da haste. A partir desses gráficos, fica claro que a tarefa foi concluída com sucesso. Você poderia tentar implementar a mesma tarefa usando uma abordagem baseada em modelo (*model-based*) para comparar o desempenho?

<a id="figure-4"></a>
![Velocidade e posições do carrinho e da haste.](https://raw.githubusercontent.com/fabiobento/cont-int-2026-1/main/modulo_simulacao_4/imagens/rl-plot.png)
**Figura 4 - Velocidade e posições do carrinho e da haste.** 

Como o nó de predição é um *script* Python usando o modelo treinado, ele pode ser integrado a qualquer arquitetura de controle de robô de alto nível. Por exemplo, podemos ativar o controlador apenas em situações específicas ou combinar abordagens baseadas em modelo (*model-based*) e DRL dentro do mesmo *script* de controle.

### Conclusão

Nessa aula exploramos o Aprendizado por Reforço Profundo (DRL - *Deep Reinforcement Learning*). Usando o DRL, os desenvolvedores podem programar indiretamente um robô, permitindo que ele aprenda a executar tarefas de forma independente. Este método é particularmente útil para robôs complexos, como humanoides ou quadrúpedes, que possuem muitas juntas e operam em ambientes desafiadores. Neste capítulo, empregamos duas ferramentas fundamentais para essa abordagem de controle, que são o Gymnasium, para criar um ambiente de observação do robô durante várias tentativas, e a Stable-Baselines3, para implementar o processo de treinamento usando algoritmos de DRL bem conhecidos.

O aprendizado por reforço profundo ainda é um campo emergente na robótica, com espaço significativo para melhorias. Os pesquisadores estão trabalhando em novos simuladores e técnicas para refinar e acelerar o treinamento. O objetivo final do DRL é fechar a lacuna entre o desempenho de um robô em configurações controladas de laboratório e em cenários do mundo real.

### Pontos a Lembrar

* O **Gymnasium** é um *framework* que fornece ambientes padronizados para treinar agentes de aprendizado por reforço, facilitando a avaliação comparativa (*benchmarking*) e a comparação de algoritmos.
* A **Stable-Baselines3** é uma biblioteca que oferece implementações de algoritmos de DRL populares (como PPO, DQN e A2C) construídos sobre o PyTorch, simplificando o processo de treinamento de agentes.
* O **Aprendizado por Reforço Profundo (DRL)** combina o aprendizado por reforço com redes neurais profundas, permitindo que os agentes lidem com ambientes complexos e de alta dimensão, como robótica ou videogames.
* Os ambientes do Gymnasium são frequentemente usados para tarefas simuladas, mas também podem ser estendidos para interagir com sistemas do mundo real através do ROS 2, tornando possível treinar e implantar agentes DRL em robôs físicos.
* A **Otimização de Política Proximal (PPO - *Proximal Policy Optimization*)**, disponível na Stable-Baselines3, é um algoritmo de DRL amplamente utilizado devido ao seu equilíbrio entre desempenho e estabilidade, especialmente em tarefas de controle contínuo.
* O DRL permite que os robôs aprendam tarefas de forma autônoma interagindo com o ambiente, em vez de seguir regras criadas manualmente, o que é particularmente útil em ambientes dinâmicos ou não estruturados.
* A combinação de DRL com abordagens baseadas em modelo pode melhorar o desempenho, aproveitando tanto as políticas aprendidas quanto a dinâmica do sistema para otimizar o controle.
* Ao usar a Stable-Baselines3 em ambientes ROS 2, a integração cuidadosa entre o agente e o *feedback* (retorno) do mundo real do robô é fundamental para garantir uma operação segura e confiável.