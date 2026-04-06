# Módulo 2: Simulação, Visualização e Cinemática Diferencial

## 1. Introdução
Neste módulo vamos trabalhar com a **modelagem de sistemas robóticos**. Como engenheiros eletricistas, trataremos o robô como um sistema dinâmico multivariável (MIMO) onde sinais de controle em malha aberta ou fechada operam sobre uma planta física simulada. Utilizaremos o **ROS 2 Jazzy** e o **Ubuntu 24.04** para validar essas teorias.

---

## 2. Modelagem Cinemática: O Robô Uniciclo
O **TurtleBot3 Waffle** utiliza tração diferencial. Sua manobrabilidade no plano $XY$ é restrita pelo acoplamento mecânico das rodas. Conforme detalhado na **Figura 1**, o movimento depende da decomposição de velocidades nos eixos locais.

![](https://github.com/fabiobento/cont-int-2026-1/raw/main/modulo_simulacao_1/imagens/cinematica-tração-diferencial.png)
*Figura 1: Modelo cinemático de um robô uní-ciclóide de tração diferencial. Adaptado de Siegwart et al. (2011).*

### 2.1. Definição de Parâmetros
* $r$: Raio nominal das rodas ($m$).
* $L$: *Wheelbase* (distância entre os centros das rodas, em $m$).
* $\vec{\xi} = [x, y, \theta]^T$: Vetor de estado (Pose) no referencial global.

### 2.2. Jacobiano da Cinemática
A relação entre as velocidades no referencial do robô ($v, \omega$) e as velocidades angulares das rodas ($\omega_R, \omega_L$) é definida pelas matrizes de transformação:

**Cinemática Direta (Forward Kinematics):**
Calcula a velocidade do chassi a partir dos encoders:
$$\begin{bmatrix} v \\ \omega \end{bmatrix} = \begin{bmatrix} \frac{r}{2} & \frac{r}{2} \\ \frac{r}{L} & -\frac{r}{L} \end{bmatrix} \begin{bmatrix} \omega_R \\ \omega_L \end{bmatrix}$$

**Cinemática Inversa (Inverse Kinematics):**
Mapeia comandos de trajetória para sinais de controle dos motores:
$$\begin{bmatrix} \omega_R \\ \omega_L \end{bmatrix} = \frac{1}{r} \begin{bmatrix} 1 & \frac{L}{2} \\ 1 & -\frac{L}{2} \end{bmatrix} \begin{bmatrix} v \\ \omega \end{bmatrix}$$

---

## 3. O Ecossistema de Simulação
Para uma simulação de alta fidelidade, o ROS 2 coordena três pilares fundamentais. A **Figura 2** ilustra como esses processos são distribuídos no Grafo de Computação.


*Figura 2: Arquitetura de software para simulação em ROS 2. O Gazebo atua como a planta física, enquanto o RViz2 serve como interface de telemetria de sensores.*

| Componente | Papel no Sistema | Sinais Gerados |
| :--- | :--- | :--- |
| **Gazebo** | Motor de Física (ODE) | Dados brutos (`/scan`, `/imu`) |
| **Robot State Publisher** | Gerenciador de Frames (TF) | Transformadas de coordenadas (`/tf`) |
| **RViz2** | Interface de Diagnóstico | Renderização de telemetria |

### Fluxo de Informação (Pipeline):
1.  **Comando:** Nó Python $\rightarrow$ `/cmd_vel` (`geometry_msgs/msg/Twist`).
2.  **Planta:** **Gazebo** processa a física e move o modelo URDF.
3.  **Realimentação:** Gazebo publica a pose em `/odom` (`nav_msgs/msg/Odometry`).
4.  **Visualização:** O **RViz2** subscreve aos tópicos para monitoramento em tempo real.

---

## 4. Estimativa de Pose e Odometria
A odometria é a integração numérica das velocidades para estimar a posição relativa. No referencial global, as equações diferenciais não-lineares projetam o movimento do robô conforme mostrado na **Figura 3**.


*Figura 3: Representação da integração de trajetória. O deslocamento instantâneo é projetado no plano XY com base na orientação $\theta$.*

$$\dot{\vec{\xi}} = \begin{bmatrix} \dot{x} \\ \dot{y} \\ \dot{\theta} \end{bmatrix} = \begin{bmatrix} \cos\theta & 0 \\ \sin\theta & 0 \\ 0 & 1 \end{bmatrix} \begin{bmatrix} v \\ \omega \end{bmatrix}$$

### Integração Discreta (Método de Euler)
Dado um tempo de amostragem $\Delta t$ (frequência do tópico `/odom`), a atualização da pose é:
* $x_{k+1} = x_k + v_k \cos(\theta_k) \Delta t$
* $y_{k+1} = y_k + v_k \sin(\theta_k) \Delta t$
* $\theta_{k+1} = \theta_k + \omega_k \Delta t$

> **Desafio de Controle:** Em sistemas reais (e simulações complexas), o erro acumulado (**Drift**) é inevitável. Sensores exteroceptivos (LiDAR/Câmeras) são necessários para corrigir a odometria em missões de longa duração.

---

## Referências Bibliográficas
* **SIEGWART, R.; NOURBAKHSH, I. R.** *Introduction to Autonomous Mobile Robots*. MIT Press, 2011.
* **CORKE, P.** *Robotics, Vision and Control*. Springer, 2017.
* **ROS 2 Documentation.** *Jazzy Jalisco Tutorials*. [docs.ros.org](https://docs.ros.org).