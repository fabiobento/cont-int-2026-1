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
![](https://github.com/fabiobento/cont-int-2026-1/raw/main/conceitos-basicos/imagens/ros-actions.png)

### Dinâmica de Funcionamento

* **Action Client:** Inicia a tarefa enviando um objetivo, monitora o progresso via feedback e tem o poder de cancelar a operação.
* **Action Server:** Executa a lógica pesada, publica atualizações de progresso e reporta o desfecho final.

> **Exemplos Práticos:** Navegação autônoma (SLAM), movimentação de juntas em braços robóticos ou sequências complexas de decolagem em drones.

### Interagindo com ROS 2 Actions

Assim como ocorre com um serviço ROS, podemos interagir com uma **action** do ROS 2 através do comando `ros2 action`. Para listar a ação com seus respectivos tipos, você pode usar:

```bash
ros2 action list -t
```

Se você estiver executando o nó `turtlesim`, encontrará a seguinte ação e seu tipo:

```bash
/turtle1/rotate_absolute [turtlesim/action/RotateAbsolute]
```

Se desejar visualizar os campos da ação, utilize o comando:

```bash
ros2 interface show turtlesim/action/RotateAbsolute

```

Você obterá a seguinte saída:

```bash
# O ângulo desejado (heading) em radianos
float32 theta
---
# O deslocamento angular em radianos em relação à posição inicial
float32 delta
---
# A rotação restante em radianos
float32 remaining
```

A definição da ação acima possui três campos principais:

1. **Goal Request (Objetivo):** O primeiro campo (`theta`).
2. **Result (Resultado):** O segundo campo (`delta`).
3. **Feedback:** O terceiro campo (`remaining`).

Esta definição de ação serve para rotacionar a tartaruga em um ângulo específico. Assim que enviamos o ângulo de destino, o cliente começará a receber o **feedback** sobre o ângulo que ainda resta. Isso é armazenado na variável `remaining`. Após concluir a rotação, o **resultado** será armazenado na variável `delta`, que representa o deslocamento angular em radianos desde a posição inicial.

Assim como no serviço ROS 2, você pode usar o comando `ros2 action` para enviar os valores do objetivo (neste exemplo, 1.57 radianos). O comando `send_goal` é utilizado para disparar a ação:

```bash
ros2 action send_goal --feedback /turtle1/rotate_absolute turtlesim/action/RotateAbsolute "{theta: 1.5708}"
```

Assim que você executar o comando, verá a tartaruga rotacionando 90 graus no sentido anti-horário e, em seguida, verá uma mensagem como esta no terminal:

**Feedback:**

```bash
remaining: 0.018799901008605957
Result:
delta: -3.1040000915527344
Goal finished with status: SUCCEEDED
```

Outro comando que você pode testar é o `ros2 action info`, que exibe informações sobre esta **action** do ROS 2, como qual nó é o **action server** (servidor da ação) e qual nó é o **action client** (cliente da ação):

```bash
ros2 action info /turtle1/rotate_absolute
```

Podemos consultar a página [_**Understanding actions**_](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.html) da documentação oficial do ROS 2 para saber mais sobre as actions.

Até agora, cobrimos brevemente os conceitos de **topic**, **service** e **action**. Agora, podemos discutir outro conceito útil: o **ROS parameter** (parâmetro ROS).

## O que é um parâmetro ROS?

Um nó do ROS pode ser configurado utilizando parâmetros. Ele pode armazenar tipos como inteiros, floats, booleanos, strings e listas. O nó pode ler esses parâmetros e controlar o fluxo do programa. Os valores desses parâmetros podem ser definidos (*set*) ou obtidos (*get*) através da ferramenta de linha de comando `ros2 param`.

Comumente, em aplicações robóticas, utilizamos um arquivo **YAML** para conter esses parâmetros. O motivo principal é que haverá múltiplos parâmetros por nó, e podem existir vários nós dentro de uma aplicação. Manter os parâmetros dentro de um arquivo YAML oferece grande flexibilidade para salvar e carregar as configurações durante a inicialização do nó.

Os arquivos de **launch** do ROS ajudam a carregar múltiplos nós junto com todos esses arquivos de parâmetros. No ROS 2, os parâmetros são armazenados nos próprios nós e, sempre que houver uma alteração em um parâmetro, ela pode ser tratada dentro do nó usando um **callback**, se necessário. Veremos mais sobre arquivos de launch na próxima seção.

Veremos agora os comandos de linha de comando do ROS 2 para listar, definir e obter parâmetros.

Para listar os parâmetros dos nós que estão em execução:
```bash
ros2 param list
```

Aqui estão os principais parâmetros do nó `turtlesim`:

```bash
turtlesim:
background_b
background_g
background_r
holonomic
................
```

Você pode notar os valores de cores **r, g, b** (red, green, blue) como parâmetros, que se referem à cor de fundo do `turtlesim`. Podemos alterar esses valores através da linha de comando e a cor de fundo mudará instantaneamente.

Aqui está a sintaxe e um exemplo de como definir o valor de um parâmetro:

```bash
ros2 param set <nome_do_nó> <nome_do_parâmetro> <valor>
ros2 param set /turtlesim background_r 150
```

Após definir o elemento vermelho (**red**) do fundo para 150, você verá que a cor de fundo muda de azul para violeta.


Além disso, se você quiser recuperar o valor de algum parâmetro, pode usar o comando `ros2 param get`. Veja a sintaxe:

```bash
ros2 param get <nome_do_nó> <nome_do_parâmetro>
```

Neste exemplo, estamos recuperando o mesmo parâmetro que acabamos de configurar e obteremos o valor definido como saída:

```bash
ros2 param get /turtlesim background_r
```

A saída será algo assim:

```bash
Integer value is: 150
```

Podemos até inicializar os parâmetros do ROS 2 durante a execução do nó, passando-os como argumentos de linha de comando. Para isso, utilizamos `--ros-args -p` para indicar os parâmetros desejados.

Veja um exemplo de uso para abrir o `turtlesim` com o fundo totalmente branco (255, 255, 255):

```bash
ros2 run turtlesim turtlesim_node --ros-args -p background_r:=255 -p background_g:=255 -p background_b:=255
```

Você pode aprender mais sobre os parâmetros do ROS consultando a [documentação oficial aqui](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Parameters/Understanding-ROS2-Parameters.html).

