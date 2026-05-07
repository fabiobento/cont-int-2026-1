# Navegação Autônoma com Aprendizado por Reforço (RL) no ROS 2

## 1. A Modelagem do Problema (MDP) para Robótica Móvel
Para que o algoritmo de RL (neste caso, o Proximal Policy Optimization - PPO) consiga controlar o nosso `lab_bot`, precisamos de modelar o problema de navegação como um Processo de Decisão de Markov (MDP), definindo três pilares:

### A. O Espaço de Observação (State Space)
O robô precisa de "ver" o mundo para tomar decisões. A nossa observação contínua será um vetor $S_t$ composto por:
* As medições do LiDAR: Vamos reduzir os 360 raios do laser para, por exemplo, 20 raios distribuídos uniformemente, capturando a distância para os obstáculos mais próximos.
* A Odometria relativa: A distância euclidiana $d$ até ao alvo e o ângulo relativo $\theta_{erro}$ entre a frente do robô e o alvo.

### B. O Espaço de Ações (Action Space)
Para simplificar o espaço de busca inicial da rede neural, vamos utilizar um espaço de ações discreto. O agente pode escolher uma de três ações no instante $t$:
* $a_0$: Avançar em linha reta ($v > 0, \omega = 0$)
* $a_1$: Virar à esquerda ($v > 0, \omega > 0$)
* $a_2$: Virar à direita ($v > 0, \omega < 0$)

### C. A Função de Recompensa (Reward Function)
A função de recompensa $R_t$ dita o comportamento. Se desenharmos mal esta função, o robô pode aprender a andar em círculos para evitar colisões sem nunca chegar ao destino. Uma função clássica e eficaz é:

$$
R_t = 
\begin{cases} 
+100, & \text{se a distância ao alvo } d < 0.2\text{m (Sucesso)} \\
-50, & \text{se a medição mínima do LiDAR } < 0.15\text{m (Colisão)} \\
C \cdot (d_{t-1} - d_t), & \text{recompensa de aproximação progressiva}
\end{cases}
$$

Onde $C$ é uma constante de escala. Esta função pune severamente as colisões, recompensa o sucesso e dá "migalhas de pão" (recompensas pequenas) sempre que o robô dá um passo na direção certa, acelerando a convergência.

## 2. A Arquitetura ROS-Gym
O `Stable-Baselines3` bloqueia a *thread* principal durante o treino. No ROS 2 Jazzy, isso causaria o erro de concorrência (`Executor is already spinning`) que vimos em arquiteturas passadas. A solução é encapsular um nó do ROS 2 (`rclpy.Node`) dentro do ambiente `gym.Env` e utilizar o método `rclpy.spin_once(timeout_sec=0)` para processar os tópicos do LiDAR e Odometria sempre que a função `step()` for chamada pelo algoritmo de RL.

## 3. Referências Bibliográficas
* SCHULMAN, J. et al. "Proximal Policy Optimization Algorithms". arXiv preprint arXiv:1707.06347, 2017.
* Documentação Stable-Baselines3: https://stable-baselines3.readthedocs.io/