# Aula 4: Simulação, Inspeção e Cinemática de Robôs Móveis

## 1. Introdução: O Robô como Sistema Dinâmico
Neste módulo, abordaremos o robô como um **sistema dinâmico multivariável (MIMO - Multiple Input, Multiple Output)**. Como engenheiros, nosso foco recai sobre a interação entre sinais de controle (entradas) e a resposta da planta física (saídas). Utilizaremos o **TurtleBot3 Waffle** no ambiente **Ubuntu 24.04** como plataforma de validação.

O Waffle opera sob o princípio da **tração diferencial**: a locomoção e a taxa de giro dependem exclusivamente do diferencial de velocidades entre duas rodas motorizadas independentes, montadas em um eixo comum.

## 2. Modelagem Cinemática e Geometria
A cinemática estuda o movimento do robô sem considerar as forças (massas e torques) que o causam. Para isso, precisamos de um modelo geométrico preciso.

### 2.1. Parâmetros Fundamentais e Referenciais
Para descrever o estado do sistema, definimos:

* **$r$ (Raio da roda):** Distância escalar entre o centro do eixo motor e o ponto de contato do pneu com o solo. No Waffle, **$r \approx 0.033$ m**.
* **$L$ (Wheelbase / Bitola):** Distância transversal entre os centros das duas rodas motrizes. Este parâmetro define o "braço de alavanca" para o giro: quanto maior $L$, mais estável é o robô em linha reta, porém menos ágil em curvas. No Waffle, **$L \approx 0.287$ m**.
* **$\vec{\xi} = [x, y, \theta]^T$ (Vetor de Pose):** Define o estado completo do robô em um plano bidimensional no referencial global (inercial):
    * **$x, y$**: Coordenadas cartesianas do centro do eixo do robô em relação à origem do mundo ($m$).
    * **$\theta$**: Orientação (*heading*) ou ângulo de guinada (*yaw*), medido entre o eixo longitudinal do robô e o eixo $X$ global ($rad$).


![](https://github.com/fabiobento/cont-int-2026-1/raw/main/modulo_simulacao_1/imagens/parametros-fundamentais.png)

**Figura 1: Diagrama técnico de um robô móvel com tração diferencial, vista superior, legendado com o raio da roda $r$, a distância entre as rodas $L$ e um sistema de coordenadas global mostrando $x$, $y$ e o ângulo de orientação (ou proa) $\theta$.** (Fonte: [Gerado por IA (Gemini, 2026)](https://gemini.google.com/))

### 2.2 Restrições Não Holonômicas

Para entender o que são **restrições não holonômicas**, imagine a diferença entre o movimento de um **drone** e o de um **carro**.

> Enquanto um drone pode se mover instantaneamente em qualquer direção (para frente, para o lado ou para cima), um carro não pode simplesmente "deslizar" para o lado para entrar em uma vaga de estacionamento; ele precisa manobrar, mudando sua orientação para conseguir um deslocamento lateral. Essa limitação é o que chamamos de restrição não holonômica.

#### O Conceito Geométrico
Na robótica e na mecânica clássica, o estado de um robô é definido pelo seu **espaço de configuração** (comumente chamado de *Pose*), que inclui sua posição $(x, y)$ e sua orientação $(\theta)$.

* **Sistema Holonômico:** O número de graus de liberdade controláveis é igual ao número total de graus de liberdade do sistema. O robô pode se mover em qualquer direção do seu espaço de configuração instantaneamente.
* **Sistema Não Holonômico:** O robô tem restrições que dependem da **velocidade** e não apenas da posição. Isso significa que, embora ele possa alcançar qualquer ponto no plano, ele não pode seguir qualquer *trajetória* infinitesimal.

#### A Restrição de "Não Deslizamento"

No caso de robôs com rodas (como o TurtleBot3 ou um carro), a restrição não holonômica surge do contato da roda com o chão. Matematicamente, a velocidade lateral no referencial do robô deve ser sempre zero:

$$\dot{x}\sin(\theta) - \dot{y}\cos(\theta) = 0$$

Essa equação diz que o robô só pode se mover na direção em que suas rodas estão apontadas. Ele está "preso" à sua orientação atual para definir seu próximo movimento linear.


Para deduzir a equação da restrição não holonômica de "não deslizamento lateral", precisamos decompor as velocidades do robô em dois referenciais: o **Global** ($\{G\}$) e o **Local/Robô** ($\{R\}$).

Aqui está o passo a passo matemático dessa dedução:

##### 1. Definição dos Referenciais e do Vetor de Pose
O estado do robô (pose) é definido no referencial global por $\vec{\xi} = [x, y, \theta]^T$. As derivadas temporais dessas coordenadas representam as velocidades no referencial global:
* $\dot{x}$: Velocidade no eixo $X$ global.
* $\dot{y}$: Velocidade no eixo $Y$ global.
* $\dot{\theta}$: Velocidade angular (rotação).

##### 2. A Matriz de Rotação
Para relacionar o que acontece no referencial global com o que o robô "sente" no seu referencial local (fixo no chassi), utilizamos a matriz de rotação $R(\theta)$. A relação entre a velocidade no referencial do robô ($V_R$) e a velocidade no referencial global ($\dot{\xi}$) é:

$$\dot{\xi} = R(\theta) \cdot V_R \implies \begin{bmatrix} \dot{x} \\ \dot{y} \\ \dot{\theta} \end{bmatrix} = \begin{bmatrix} \cos\theta & -\sin\theta & 0 \\ \sin\theta & \cos\theta & 0 \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} v_{longitudinal} \\ v_{lateral} \\ \omega \end{bmatrix}$$

##### 3. A Restrição Física de Não Deslizamento
A restrição de "não deslizamento" (em inglês, *no-skidding*) assume que as rodas do robô (como as do TurtleBot3 Waffle) têm atrito lateral infinito, o que impede que o robô deslize para os lados como um disco de hóquei no gelo.

Portanto, a **velocidade lateral no referencial do robô** ($v_{lateral}$) deve ser obrigatoriamente **zero**:
$$v_{lateral} = 0$$

##### 4. Isolando a Velocidade Lateral
Para encontrar a equação $\dot{x}\sin(\theta) - \dot{y}\cos(\theta) = 0$, precisamos inverter a relação do passo 2 para isolar $v_{lateral}$. Multiplicamos ambos os lados pela transposta da matriz de rotação ($R(\theta)^T$):

$$\begin{bmatrix} v_{longitudinal} \\ v_{lateral} \\ \omega \end{bmatrix} = \begin{bmatrix} \cos\theta & \sin\theta & 0 \\ -\sin\theta & \cos\theta & 0 \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} \dot{x} \\ \dot{y} \\ \dot{\theta} \end{bmatrix}$$

Focando apenas na segunda linha da matriz resultante (que define $v_{lateral}$):
$$v_{lateral} = (-\sin\theta) \cdot \dot{x} + (\cos\theta) \cdot \dot{y}$$


##### 5. Finalização da Equação
Como estabelecemos no passo 3 que $v_{lateral} = 0$, temos:
$$-\dot{x}\sin(\theta) + \dot{y}\cos(\theta) = 0$$

Multiplicando a equação inteira por $-1$ para ajustar ao formato padrão:
$$\dot{x}\sin(\theta) - \dot{y}\cos(\theta) = 0$$

##### O que essa equação nos diz?
Essa é uma restrição **não holonômica** porque ela impõe um limite às velocidades instantâneas do robô ($\dot{x}, \dot{y}$) com base na sua posição atual ($\theta$). Note que ela não impede o robô de chegar a qualquer ponto $(x,y)$ no laboratório, mas diz que ele não pode chegar lá "andando de lado"; ele precisa manobrar sua orientação $\theta$ para que sua velocidade linear aponte na direção desejada.



![](https://github.com/fabiobento/cont-int-2026-1/raw/main/modulo_simulacao_1/imagens/restricao-n-holo.png)

**Figura 2: Representação esquemática de um robô móvel com tração diferencial, mostrando a restrição não holonômica de não deslizamento lateral.** (Fonte: [Gerado por IA (Gemini, 2026)](https://gemini.google.com/))

#### Implicações no Controle e Planejamento
As restrições não holonômicas tornam o controle de robôs muito mais desafiador por dois motivos principais:

1.  **Dependência da Trajetória:** Para chegar a uma posição lateral, o robô deve descrever uma curva (combinação de $v$ e $\omega$). O caminho importa tanto quanto o destino.
2.  **Estacionamento e Manobras:** É por causa dessa restrição que precisamos fazer a "baliza". Se um carro fosse holonômico, ele apenas se moveria lateralmente para dentro da vaga. Como não é, ele precisa de uma sequência de movimentos curvos para compensar a impossibilidade de translação lateral pura.

#### Comparação Prática

| Característica | Sistema Holonômico | Sistema Não Holonômico |
| :--- | :--- | :--- |
| **Exemplo** | Drone, Robô com rodas Mecanum | Carro, Bicicleta, TurtleBot3 |
| **Movimento lateral** | Instantâneo | Requer manobra/mudança de $\theta$ |
| **Complexidade** | Simples de planejar trajetória | Complexo (requer cinemática inversa) |
| **Graus de Liberdade** | Controláveis = Totais | Controláveis < Totais |


### Resumo para Engenharia
Em termos de cálculo, uma restrição é **não holonômica** quando ela é expressa como uma equação diferencial (envolvendo velocidades) que **não pode ser integrada** para se tornar uma restrição apenas de posição. Ou seja, ela é uma restrição de "caminho" que não reduz a dimensão do espaço que o robô pode eventualmente alcançar, apenas limita como ele pode navegar por esse espaço a cada instante.


### 2.2. O Jacobiano: Acoplamento de Velocidades
Um robô diferencial possui **restrições não-holonômicas**: ele tem menos graus de liberdade controláveis do que o total de graus de liberdade do plano (ex: ele não pode "deslizar" lateralmente sem girar).

As variáveis operacionais são:
* **$\omega_R, \omega_L$**: Velocidades angulares das rodas direita e esquerda, respectivamente ($rad/s$).
* **$v$**: Velocidade escalar linear do chassi no sentido do seu eixo longitudinal ($m/s$).
* **$\omega$**: Velocidade escalar angular do chassi em torno do seu centro de massa ($rad/s$).

#### **Cinemática Direta (Forward Kinematics)**
Estima as velocidades resultantes do chassi a partir da leitura dos *encoders* das rodas:

$$\begin{bmatrix} v \\ \omega \end{bmatrix} = \begin{bmatrix} \frac{r}{2} & \frac{r}{2} \\ \frac{r}{L} & -\frac{r}{L} \end{bmatrix} \begin{bmatrix} \omega_R \\ \omega_L \end{bmatrix} \implies \begin{cases} v = \frac{r}{2}(\omega_R + \omega_L) \\ \omega = \frac{r}{L}(\omega_R - \omega_L) \end{cases}$$

#### **Cinemática Inversa (Inverse Kinematics)**
Representa a lei de controle: traduz a trajetória desejada ($v, \omega$) nos comandos de velocidade que devem ser impostos aos motores:

$$\begin{bmatrix} \omega_R \\ \omega_L \end{bmatrix} = \frac{1}{r} \begin{bmatrix} 1 & \frac{L}{2} \\ 1 & -\frac{L}{2} \end{bmatrix} \begin{bmatrix} v \\ \omega \end{bmatrix} \implies \begin{cases} \omega_R = \frac{1}{r}(v + \frac{\omega L}{2}) \\ \omega_L = \frac{1}{r}(v - \frac{\omega L}{2}) \end{cases}$$

## 3. Implementação em Python
No ROS 2, a camada de abstração de hardware permite que enviemos comandos de alto nível. O nó de controle do TurtleBot3 recebe mensagens do tipo `geometry_msgs/msg/Twist` no tópico `/cmd_vel` e executa internamente as equações da cinemática inversa acima.

### **Exemplo Numérico de Projeto: Trajetória Circular**
Para projetar um círculo de raio **$R = 0.375$ m**, arbitramos uma velocidade linear **$v = 0.15$ m/s**.
A velocidade angular alvo será:
$$\omega = \frac{v}{R} = \frac{0.15}{0.375} = 0.4 \text{ rad/s}$$

Ao publicar este comando, o firmware do robô converterá esses valores para a rotação das rodas. Para a roda direita ($\omega_R$), o cálculo será:
$$\omega_R = \frac{1}{0.033} \left( 0.15 + \frac{0.287 \cdot 0.4}{2} \right) \approx 6.28 \text{ rad/s}$$


![](https://github.com/fabiobento/cont-int-2026-1/raw/main/modulo_simulacao_1/imagens/pipeline-controle.png)

**Figura 3: Fluxograma infográfico de um pipeline de controle de robô em ROS 2: Nó (script Python) $\rightarrow$ /cmd_vel (mensagem do tipo Twist) $\rightarrow$ Controlador do Robô $\rightarrow$ PWM do Motor/Rotação das Rodas $\rightarrow$ Simulação no Gazebo..** (Fonte: [Gerado por IA (Gemini, 2026)](https://gemini.google.com/))



## 4. Odometria e Discretização do Tempo
A odometria é a estimativa da pose $\vec{\xi}$ baseada na integração das velocidades. Como sistemas computacionais são discretos, trabalhamos com um intervalo de amostragem **$\Delta t$** (definido pelo *timer* do script Python, ex: $0.1$ s).

### 4.1. Integração pelo Método de Euler
A cada passo de tempo $k$, o estado é atualizado:
* $x_{k+1} = x_k + v_k \cos(\theta_k) \Delta t$
* $y_{k+1} = y_k + v_k \sin(\theta_k) \Delta t$
* $\theta_{k+1} = \theta_k + \omega_k \Delta t$

> **Nota Crítica sobre Deriva (*Drift*):** Na teoria, a integração é perfeita. Na prática, erros de arredondamento numérico, frequência de amostragem limitada e micro-escorregamentos simulados no Gazebo fazem com que o erro se acumule. Por isso, após várias voltas, o rastro da odometria raramente fecha um círculo perfeito.

## 5. Ecossistema de Simulação e Referenciais
O ROS 2 Jazzy coordena três ferramentas fundamentais:

| Componente | Papel no Sistema | Sinais Gerados |
| :--- | :--- | :--- |
| **Gazebo** | Motor de Física (**A Planta**) | Simula inércia, colisões e publica `/scan` |
| **Robot State Publisher** | Gerenciador de Frames (**TF**) | Publica a relação espacial entre as partes do robô |
| **RViz2** | Interface de Telemetria | Renderiza a percepção dos sensores |

### Referenciais de Coordenadas (Frames)
No RViz2, o **Fixed Frame** altera sua percepção do movimento:
* **Frame `odom` (Global):** Referencial inercial fixo no mapa. Vemos o robô se deslocando sobre o grid.
* **Frame `base_link` (Local):** Referencial fixo no centro do robô. O robô parece estático, e o mundo inteiro (incluindo as leituras de laser) gira e se move ao redor dele.

![](https://github.com/fabiobento/cont-int-2026-1/raw/main/modulo_simulacao_1/imagens/fixed-frames.png)

**Figura 4: Referenciais fixos no RViz: o lado esquerdo mostra o referencial fixo `odom` com o robô se movendo sobre uma grade; o lado direito mostra o referencial fixo `base_link` com o robô estático no centro e a `grid/laserscan` rotacionando ao seu redor.** (Fonte: [Gerado por IA (Gemini, 2026)](https://gemini.google.com/))


## 6. Resumo do Pipeline de Dados
Para o sucesso do laboratório, visualize o fluxo:
1.  **Algoritmo (Python):** Calcula $v$ e $\omega$ baseados na geometria desejada.
2.  **Bridge:** Converte o sinal ROS para o ambiente Gazebo.
3.  **Física (Gazebo):** Simula o movimento e a interação com o ambiente.
4.  **Feedback (Odometria):** Calcula o deslocamento das rodas e publica a pose em `/odom`.
5.  **Visualização (RViz2):** Renderiza o rastro histórico, permitindo comparar a teoria (raio projetado) com a prática (raio medido).

---
**Referências Bibliográficas**
* SIEGWART, R.; NOURBAKHSH, I. R. *Introduction to Autonomous Mobile Robots*. MIT Press, 2011.
* CORKE, P. *Robotics, Vision and Control*. Springer, 2017.