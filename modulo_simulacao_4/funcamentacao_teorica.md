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

<a id="figure-19-2"></a>
![](https://raw.githubusercontent.com/fabiobento/cont-int-2026-1/main/modulo_simulacao_4/imagens/cart-pole.png)
**Figura 2 - O pêndulo invertido usado na aplicação de DRL.** 

Vamos começar criando um pacote ROS 2 para armazenar o modelo e os arquivos de simulação.

`$ ros2 pkg create cartpole_description`

Este pacote conterá o modelo *xacro* do robô e um arquivo *launch* que inicia a simulação e os diferentes controladores. O arquivo do modelo é básico e consiste em duas juntas:

* **linear:** Uma junta prismática para mover o carrinho sobre o trilho.
* **pivot:** Uma junta contínua permitindo a rotação do pêndulo em torno do carrinho.

O pêndulo pode se mover livremente sem nenhuma entrada de controle direto e se mantém equilibrado através do movimento do carrinho. Quando o carrinho é empurrado para um lado, o pêndulo naturalmente se inclina na direção oposta. O arquivo `cartpole.urdf.xacro` define as juntas e os elos para este sistema, e você pode encontrar o arquivo completo no repositório do GitHub do curso. Como ele é longo e já cobrimos como criar tais arquivos, a principal diferença aqui é a interface de controle para as juntas. Neste caso, habilitamos o controle de esforço, que é refletido na seção `ros2_control` do arquivo *xacro*, conforme mostrado no código a seguir. Como de costume, a *tag* `ros2_control` é usada para definir como as juntas são controladas. Incluímos a interface de *hardware* para fazer a interface com as juntas simuladas.

```xml
<ros2_control name="IgnitionSystem" type="system">
<hardware>
<plugin>ign_ros2_control/IgnitionSystem</plugin>
</hardware>

```

A junta linear é comandada usando uma entrada de controle de esforço. No entanto, estamos interessados em saber sua posição ao longo do trilho para posicioná-la no meio do trilho no início de um novo episódio de treinamento.

```xml
<joint name="linear">
<command_interface name="effort" />
<state_interface name="position"><param name="initial_value">0.0</param>
</state_interface>
<state_interface name="velocity"/>
<state_interface name="effort"/>
</joint>

```

A mesma interface de controle é usada para a junta rotacional conectada ao pêndulo. Embora não precisemos de um controlador para esta junta (já que o objetivo é estabilizar o pêndulo indiretamente movendo o carrinho para a esquerda ou para a direita), o sistema deve iniciar com o pêndulo em uma posição estável, que é um ângulo de 0.0, conforme mostrado na Figura 16.2. Usando o controlador de esforço, o pêndulo ainda estará livre para se mover ao redor do carrinho durante a simulação.

```xml
<joint name="pivot">
<command_interface name="effort" />
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
<gazebo>
<plugin filename="ign_ros2_control-system"
name="ign_ros2_control::IgnitionROS2ControlPlugin">
<parameters>$(find cartpole_description)/config/cartpole_controller.yaml</parameters>
</plugin>
</gazebo>

```

Junto com o modelo do robô, devemos criar um arquivo *launch* para iniciar a simulação e os controladores de esforço para a base e para a haste do pêndulo. No pacote do repositório do GitHub, chamamos este arquivo de `cartpole.launch.py`. Após editar o `CMakeLists.txt` para instalar os diretórios `urdf` e `launch`, você pode iniciar a simulação usando os seguintes comandos:

`$ colcon build --symlink-install`
`$ source install/setup.bash`
`$ ros2 launch cartpole_description cartpole.launch.py`

Da simulação, usaremos os seguintes tópicos:

* `/effort_control/commands` : Para controlar o esforço da base para mover o carrinho.
* `/stick_effort_control/commands` : Para controlar a haste em torno do pêndulo na fase de *reset* (reinício).
* `/joint_states` : Para ler o estado do sistema, obtendo as observações dele.

Outro aspecto chave da simulação é que o modelo do robô deve ser fisicamente controlável. Isso depende muito dos parâmetros dinâmicos do modelo. Por exemplo, se o carrinho for muito leve e o pêndulo for muito pesado, será impossível controlar a orientação do pêndulo, mesmo com uma abordagem de DRL. Isso destaca a importância de ter um modelo de simulação preciso para um controle bem-sucedido.

Após obter um modelo de simulação correto, precisamos de uma função para reiniciar o estado do sistema: o carrinho no meio do trilho e o pêndulo perpendicular ao carrinho. Por esse motivo, criaremos um novo pacote que recebe um sinal como entrada para reiniciar o estado da simulação.

`$ ros2 pkg create --build-type ament_python cartpole_reset --dependencies rclpy std_msgs`

Este pacote contém o nó `cartpole_reset.py`. Seu conteúdo é discutido a seguir:

1. Primeiro, importamos os módulos Python necessários. O tipo de dados `Float64MultiArray` é usado para enviar comandos às juntas do controlador. Embora tenhamos uma junta por controlador, ainda precisamos preencher o *array* com um único elemento para cada junta.

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray, Bool
from sensor_msgs.msg import JointState
from threading import Thread
import math

```

2. Precisamos de uma função adequada para reportar o ângulo do estado da junta dentro de um limite adequado. Conforme definido no modelo do robô, esse elo (*link*) é um elo contínuo; isso significa que, ao realizar múltiplas rotações, seu valor tende a um valor infinito. Diferentemente, precisamos que o ângulo seja delimitado no intervalo `-pi` a `pi`.

```python
def bound_angle(angle):
    bounded_angle = (angle + math.pi) % (2 * math.pi) - math.pi
    return bounded_angle

```

3. No construtor da classe, definiremos a entrada e a saída usando os dados do ROS 2.

```python
class CartPoleReset(Node):
    def __init__(self):
        super().__init__('yolo_node')
        self.js_sub = self.create_subscription(JointState, "/joint_states", self.js_cb, 10)
        self.cartpole_eff_pub = self.create_publisher(Float64MultiArray, "/effort_control/commands", 10)
        self.system_ready_pub = self.create_publisher(Bool, "/cartpole/ready", 10)
        self.cartpole__reset_sub = self.create_subscription(Bool, "/cartpole/reset", self.reset, 10)
        self.stick_eff_pub = self.create_publisher(Float64MultiArray, "/stick_effort_control/commands", 10)

```

4. Quando o carrinho está na posição de reinício, publicamos uma *flag* (bandeira) booleana para informar ao *software* de terceiros (o ambiente de treinamento neste caso) sobre o status do sistema. Se essa *flag* for verdadeira, o sistema está pronto; caso contrário, está no estado de *reset*.

```python
        self.timer = self.create_timer(0.1, self.publish_system_ready)
        self.reset = False
        self.js_ready = False
        self.js = None
        self.system_ready = Bool()
        self.system_ready.data = True

```

5. No *loop* principal, aguardamos uma nova solicitação de reinício do sistema. Naturalmente, devemos esperar até que o status do sistema esteja pronto, recebendo os estados das juntas. Essa verificação é executada em uma taxa baixa (2 Hz).

```python
    def main_loop(self):
        rate = self.create_rate(2)
        while not self.js_ready:
            rate.sleep()
        while rclpy.ok():
            if( self.reset == True):

```

6. Quando uma requisição de reinício é recebida, configuramos as funções necessárias para colocar o sistema no estado de reinício. Por este motivo, implementamos dois controladores Proporcional-Derivativo (PD). Esses PDs obtêm os erros de posição a partir dos ângulos do carrinho e do pêndulo e geram um torque adequado para manter o sistema no estado de reinício.

```python
                self.system_ready.data = False
                self.system_ready_pub.publish(self.system_ready)
                rate2 = self.create_rate(100)
                self.reset = False
                cmd = Float64MultiArray()
                stick_tau_cmd = Float64MultiArray()
                k = 0.8
                k2 = 0.2
                k_stick = 0.1
                k2_stick = 0.05
                stick_e = 0.0
                prev_stick_e = 0.0
                stick_derivative = 0.0
                cart_e = 0
                prev_cart_e = 0
                cart_e_derivative = 0

```

7. Os erros iniciais no carrinho e no pêndulo são obtidos dos estados das juntas, e o *loop* de controle principal do nó começa. A ação de controle continua até que as condições de reinício sejam atendidas — especificamente, quando o pêndulo estiver na posição de reinício e sua velocidade for quase zero. E quanto à posição do carrinho no trilho? Não definimos isso explicitamente, pois não estamos focados em ter o carrinho exatamente na posição 0.0. No entanto, se o carrinho se mover muito em direção ao centro do trilho, isso fará com que o pêndulo se mova, dificultando sua estabilização e aumentando sua velocidade. Embora o carrinho não precise estar perfeitamente no 0, nosso objetivo é mantê-lo mais perto do centro.

```python
                cart_e = self.js.position[0]
                prev_cart_e = 0
                stick_js = bound_angle(self.js.position[1])
                while ( (math.fabs( stick_js) > 0.05) or (math.fabs(self.js.velocity[0]) > 0.01) ) :
                    cart_e = (self.js.position[0])
                    cart_e_derivative = (cart_e - prev_cart_e) / (1.0/100.0)

```

8. O esforço tanto para o carrinho quanto para o pêndulo é calculado usando a fórmula do controlador PD, que combina um ganho aplicado ao erro atual (a diferença entre a posição atual e a desejada) e outro ganho aplicado à derivada do erro (a taxa de variação do erro). Antes de enviar o comando de esforço, também precisamos determinar se um torque positivo ou negativo é necessário para mover o modelo simulado para a posição desejada.

```python
                    cart_tau = k*cart_e + k2*cart_e_derivative
                    cmd.data = [-cart_tau]
                    stick_js = bound_angle(self.js.position[1])
                    stick_e = math.fabs( stick_js )
                    stick_derivative = (stick_e - prev_stick_e) / (1.0/100.0)
                    tau = k_stick*stick_e + k2_stick*stick_derivative
                    if ( stick_js > 0 ):
                        tau = -tau
                    stick_tau_cmd.data = [tau]
                    self.cartpole_eff_pub.publish(cmd)
                    self.stick_eff_pub.publish(stick_tau_cmd)
                    prev_stick_e = stick_e
                    prev_cart_e = cart_e
                    rate2.sleep()
                self.system_ready.data = True
            rate.sleep()

```

9. O restante do código contém as funções para receber como entrada a solicitação de reinício, os estados das juntas e a *thread* para publicar quando a função de reinício for concluída.

```python
    def reset(self, msg):
        self.reset = True
    def js_cb(self, msg):
        self.js = msg
        self.js_ready = True
    def publish_system_ready(self):
        self.system_ready_pub.publish(self.system_ready)
    def run( self ):
        main_loop_thread = Thread(target = self.main_loop, args = ())
        main_loop_thread.start()
        rclpy.spin(self)
def main(args=None):
    rclpy.init(args=args)
    node = CartPoleReset()
    node.run()
if __name__ == '__main__':
    main()

```

Precisamos adicionar este nó ao arquivo de configuração `setup.py` e compilar o *workspace*. Embora não precisemos usar esse nó imediatamente, já que o Cart-Pole já está na sua posição inicial, vamos executá-lo mais tarde, quando os nós de treinamento e teste exigirem que o modelo simulado seja reiniciado.

Agora temos todos os elementos para integrar o Gymnasium com o ROS 2 e criar nosso primeiro ambiente.

Aqui está a tradução da seção solicitada do livro, formatada e adaptada para o português brasileiro:

## **Integrando o Gymnasium e o ROS 2**

Para integrar o Gymnasium com o ROS 2, precisamos implementar suas funções principais usando a API do ROS 2 para controlar a simulação. Isso nos permite usar a mesma interface de controle durante o teste do sistema, de modo que, se tivermos um sistema físico idêntico, possamos aplicar perfeitamente o que o agente aprendeu no ambiente simulado ao sistema do mundo real.
Vamos criar um pacote ROS 2 contendo o ambiente, o treinamento do modelo e seu uso na fase de execução.

`$ ros2 pkg create cartpole_drl_ppo --build-type ament_python --dependencies rclpy std_msgs sensor_msgs geometry_msgs`

Neste pacote, implementaremos os seguintes *scripts*:

* `cartpole_env.py` : Implementa o ambiente Gymnasium usado tanto no treinamento quanto no uso.
* `cartpole_training.py` : O nó que usa o ambiente para realizar o treinamento do sistema.
* `cartpole_prediction.py` : O nó que usa o modelo treinado para calcular a próxima ação para realizar a tarefa.

Vamos começar discutindo o script `cartpole_env.py`. Para otimizar a discussão, mostraremos apenas as partes salientes do *script*. Como de costume, verifique o repositório de código-fonte para a sua versão completa.

1. No início, junto com as dependências do ROS 2, importamos os módulos para usar o *gymnasium*. Isto é, o *gymnasium* em geral e o espaço (*space*) do Gymnasium.

```python
import gymnasium as gym
from gymnasium import spaces
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray, Bool
from threading import Thread

```

2. A classe principal herda da classe *Environment* (Ambiente) do Gymnasium. Isso dá acesso ao mecanismo interno do Gymnasium para realizar o treinamento do sistema.

```python
class CartPoleROS2Env(gym.Env):
    def __init__(self):
        super(CartPoleROS2Env, self).__init__()

```

3. Vamos definir o espaço de ação (*action space*), que especifica as possíveis ações que o robô pode tomar de forma discreta ou contínua a cada iteração. No nosso caso, temos duas ações básicas: aplicar uma força para empurrar o carrinho para a esquerda ou para a direita. No entanto, como queremos modular continuamente a força (por exemplo, aplicando mais força quando a haste está caindo), definimos o espaço de ação como um intervalo contínuo de valores de -15 N a 15 N (aproximadamente 1,5 kg de força).

```python
        self.action_space = spaces.Box(low=-15.0, high=15.0, shape=(1,), dtype=np.float32)

```

4. Também precisamos definir o espaço de observação (*observation space*), que inclui o conjunto de valores possíveis que representam o estado do robô. Isso incluirá a posição do carrinho no trilho, sua velocidade, bem como a posição e a velocidade da haste. Devemos definir limites apropriados para esses valores para garantir que o espaço de observação permaneça dentro de limites adequados.

```python
        high = np.array([5.0, 1.0, math.pi, 8.5], dtype=np.float32)
        self.observation_space = spaces.Box(-high, high, dtype=np.float32)

```

5. Agora podemos inicializar o nó ROS 2 para fazer a interface com a rede ROS 2. Neste contexto, o nó é inicializado sem argumentos. Após a inicialização, a saída (o comando de esforço do *cart-pole*) e a entrada (o espaço observado, recebido através de `joint_states`) são vinculados. Os tópicos para solicitar um novo reinício (*reset*) do sistema e receber o estado de prontidão (*readiness*) do simulador são recebidos.

```python
        rclpy.init(args=None)
        self.node = rclpy.create_node('cartpole_gym_env')
        self.cartpole_eff_pub = self.node.create_publisher(Float64MultiArray, "/effort_control/commands", 10)
        self.joint_state_sub = self.node.create_subscription(JointState, '/joint_states', self.joint_state_callback, 10 )
        self.current_observation = np.zeros(4, dtype=np.float32)
        self.state_received = False
        self.cartpole_reset_pub = self.node.create_publisher(Bool, "/cartpole/reset", 10)
        self.system_ready_sub = self.node.create_subscription(Bool, '/cartpole/ready', self.system_ready_cb, 10 )

```

6. Para permitir que o ROS 2 opere corretamente, nós o executamos em segundo plano usando um `SingleThreadedExecutor`, que gerencia os *callbacks* do nó. Uma *thread* separada é criada para executar continuamente a função `spin()` do nó, permitindo que o nó lide com mensagens e eventos de forma assíncrona enquanto o programa principal é executado.

```python
        self.executor = rclpy.executors.SingleThreadedExecutor()
        self.executor.add_node(self.node)
        self.spin_thread = threading.Thread(target=self.executor.spin, daemon=True)
        self.spin_thread.start()
        self.system_ready = False

```

7. No `joint_state_callback`, preenchemos os dados de observação. Como já dito, isso representa o estado do agente, nos dando uma recompensa positiva ou negativa. Além disso, neste caso, como no nó de *reset*, devemos limitar o ângulo da haste, fazendo com que fique dentro do intervalo adequado `-pi`, `pi`.

```python
    def joint_state_callback(self, msg):
        try:
            self.current_observation = np.array([
                msg.position[0],
                msg.velocity[0],
                bound_angle(msg.position[1]),
                msg.velocity[1]
            ], dtype=np.float32)
            self.state_received = True

```

8. Vamos agora discutir a função `step`. Lembre-se que esta função é chamada a cada iteração, realizando uma ação e avaliando as observações para entender se a ação dá ao robô uma recompensa positiva ou leva ao término do episódio. Por este motivo, esta função é executada apenas se o estado do agente estiver disponível.

```python
    def step(self, action):
        if not self.state_received:
            time.sleep(0.01)
            return self.current_observation, 0.0, False, {}

```

9. Uma vez que a ação gerada pelo agente para tentar realizar a tarefa é diretamente a força aplicada ao carrinho, nós publicamos seu valor no tópico de comando de controle de esforço, e então esperamos que a malha de controle da simulação do *ros2_control* (100 Hz) avalie as observações.

```python
        eff_msg = Float64MultiArray()
        eff_msg.data = [float(action[0])]
        self.cartpole_eff_pub.publish(eff_msg)
        obs = self.current_observation.copy()

```

10. O episódio de aprendizado é considerado encerrado se alguma das seguintes condições for atendida: a posição do carrinho for além de `[-2, 2]` metros, o ângulo da haste exceder `[π/4, -π/4]` radianos (`obs[0]` e `obs[2]`, respectivamente), a velocidade rotacional da haste for maior que `0.3` rad/s, ou a velocidade do carrinho exceder `1` m/s. Se alguma dessas observações cair fora da faixa aceitável, será impossível estabilizar a haste e impedi-la de oscilar.

```python
        done = bool(
            math.fabs(obs[0] > 2) or
            math.fabs(obs[2] > math.pi/4) or
            math.fabs( obs[3] > 0.3 ) or
            math.fabs( obs[1] > 1.0 )
        )

```

11. A cada iteração, o sistema fornece `1` ponto de recompensa se a haste estiver estável no carrinho (todas as condições do estado são válidas). Caso contrário, nenhuma recompensa é fornecida. Adicionalmente, queremos ter certeza de que a velocidade do carrinho seja a mais suave possível. Quando sua velocidade aumenta, a estabilidade da haste é difícil de manter. Por esta razão, fornecemos uma recompensa negativa se sua velocidade for maior do que o esperado.

```python
        if(done and math.fabs( obs[1] > 1.0 ) ):
            reward = -10
        elif done:
            reward = 0.0
        else:
            reward = 1.0
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
        reset_data = Bool()
        reset_data.data = True
        self.cartpole_reset_pub.publish( reset_data )
        time.sleep(0.5)
        while( not self.system_ready ):
            time.sleep(0.001)
        return self.current_observation.copy(), {}

```

14. Finalmente, na função `close`, devemos apenas sair de forma limpa do nó ROS 2.

```python
    def close(self):
        self.executor.shutdown()
        self.node.destroy_node()
        rclpy.shutdown()

```

Concluímos agora nosso primeiro ambiente Gymnasium. Isso significa que podemos escrever o procedimento para treinar o agente neste ambiente e com os dados de simulação do Gazebo, conforme discutido nas próximas seções.

### **Treinando um Robô Usando o Gymnasium e stable_baselines3**

Escrever um ambiente Gymnasium adequado é apenas um passo básico para treinar nosso robô. O próximo passo é executar recursivamente o robô no ambiente, selecionando adequadamente as ações a serem executadas, coletando as recompensas e treinando a Rede Neural Profunda que direciona as ações do robô na fase de predição, quando o robô finalmente for capaz de realizar as ações por conta própria. Para simplificar a etapa de treinamento, usaremos outra biblioteca, tipicamente conectada com o Gymnasium, que é a *Stable-Baselines3* (SB3). Trata-se de uma biblioteca Python que fornece implementações de algoritmos de aprendizado por reforço (RL) no estado da arte. Alguns dos algoritmos de DRL mais difundidos implementados na SB3 são a Otimização de Política Proximal (PPO), *Deep Q-Network* (DQN) e *Soft Actor-Critic* (SAC). A SB3 é construída sobre o PyTorch e pode ser usada diretamente em nossos nós Python do ROS 2.

**Nota:** O PyTorch é um popular *framework* de aprendizado profundo de código aberto conhecido por sua flexibilidade, gráficos de computação dinâmica e forte suporte a GPU. É amplamente utilizado para treinamento e experimentação de redes neurais em tarefas de IA.

Vamos instalar a SB3 em nosso sistema usando os seguintes comandos:

`$ pip3 install stable_baselines3`
`$ pip install 'numpy<2'`
`$ pip install stable-baselines3[extra]`

Podemos adicionar o nó para realizar a fase de treinamento no mesmo pacote do ambiente.

`$ cd ros2_ws/src/cartpole_drl_ppo`
`$ touch cartpole_drl_ppo/cartpole_training.py`

O conteúdo deste script é explicado a seguir:

1. No início, importamos o ambiente criado até agora. Adicionalmente, incluímos o módulo para realizar o método de treinamento de DRL desejado, o PPO (isto também motiva o nome do pacote). PPO significa *Proximal Policy Optimization* (Otimização de Política Proximal) e melhora os métodos de gradiente de política equilibrando exploração e estabilidade. Além disso, permite especificar um espaço de ação contínuo, diferentemente do conhecido *Deep Q-Network* (DQN), que só permite um espaço discreto. Por fim, queremos salvar o modelo diretamente no diretório de instalação do pacote. Por esse motivo, usamos o módulo `get_package_share_directory` de `ament_index_python.packages`.

```python
from cartpole_drl_ppo.cartpole_env import CartPoleROS2Env
from stable_baselines3 import PPO
from ament_index_python.packages import get_package_share_directory

```

2. Na função principal, obtemos a pasta de instalação do pacote `cartpole_drl_ppo` para podermos salvar o arquivo do modelo treinado lá. Isso nos permite carregar o modelo facilmente mais tarde, quando precisarmos usá-lo para previsões.

```python
def main(args=None):
    model_pkg_path = get_package_share_directory('cartpole_drl_ppo') + "/"

```

3. Este código inicializa um modelo PPO com uma política de rede neural (`MlpPolicy`) para interagir com o ambiente (`env`). A opção `verbose=1` fornece registro detalhado durante o treinamento. Ela prepara o agente para aprender usando o algoritmo PPO no ambiente determinado. Após a inicialização do modelo, nós o treinamos. Treinamos o modelo por 15.000 *timesteps* (passos de tempo), o que significa que o agente interagirá com o ambiente esse número de vezes. A opção `progress_bar=True` mostra uma barra de progresso para acompanhar o processo de treinamento.

```python
    env = CartPoleROS2Env()
    model = PPO('MlpPolicy', env, verbose=1)
    model.learn(total_timesteps=15000, progress_bar=True)

```

4. Finalmente, podemos salvar o modelo e fechar o ambiente.

```python
    model.save(model_pkg_path + "ppo_cartpole_ros2")
    env.close()

```

Após modificar adequadamente o arquivo `setup.py`, compilar e carregar (*sourcing*) o *workspace*, podemos agora iniciar o processo de treinamento. Obviamente, antes de iniciá-lo, devemos lançar a simulação, o nó de *reset* e, finalmente, o processo de treinamento.

`$ ros2 launch cartpole_description cartpole.launch.py`
`$ ros2 run cartpole_reset cartpole_reset`
`$ ros2 run cartpole_drl_ppo cartpole_training`

Neste ponto, o robô começa a realizar diferentes tentativas para melhorar sua experiência no ambiente Gymnasium. O tempo necessário para concluir o processo depende da velocidade com que o robô aprende e do número de passos de tempo que definimos na função de aprendizado. No entanto, no terminal onde iniciamos o processo de treinamento, você pode acompanhar o processo de aprendizado. Um exemplo dessa saída é mostrado na Figura 16.3, e é explicado a seguir.