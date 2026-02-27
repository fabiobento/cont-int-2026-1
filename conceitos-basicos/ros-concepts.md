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


Agora, vamos analisar o arquivo de **launch** do ROS na seção seguinte.

## O que é um arquivo de launch do ROS 2?

Os arquivos de **launch** do ROS 2 são ferramentas poderosas para iniciar múltiplos nós, configurar parâmetros, realizar o remapeamento de nomes de tópicos e controlar a execução de nós em um sistema robótico complexo.

Eles são extremamente úteis se a sua aplicação possuir vários nós. Não é prático executar cada nó individualmente usando o comando `ros2 run`; em vez disso, os arquivos de launch oferecem uma maneira de rodar os nós com todas as suas configurações pré-definidas através de um único comando.

O comando `ros2 launch` é utilizado para disparar um arquivo de launch. Esses arquivos ficam guardados dentro dos pacotes do ROS 2. No ROS 2, o arquivo de launch pode ser escrito em **Python**, **XML** ou **YAML**. O formato em Python oferece maior flexibilidade em comparação às outras opções, especialmente em aplicações robóticas complexas. Ao escrever um arquivo de launch em Python, a extensão será `.py` e, geralmente, segue-se a convenção de nomenclatura `*.launch.py`.

A sintaxe do comando `ros2 launch` é apresentada abaixo:

```bash
ros2 launch nome_do_pacote nome_do_arquivo_de_launch.py
```

Aqui está um exemplo de execução de um arquivo de launch que já vem incluso no pacote `demo_nodes_cpp`:

```bash
ros2 launch demo_nodes_cpp talker_listener_launch.py
```

Este arquivo iniciará simultaneamente o **talker** (emissor) e o **listener** (receptor), e você verá uma mensagem como esta no terminal:

```bash
[INFO] [launch]: Default logging verbosity is set to INFO
[INFO] [talker-1]: process started with pid [1505]
[INFO] [listener-2]: process started with pid [1506]
[talker-1] [INFO] [1726427687.713985453] [talker]: Publishing: 'Hello World: 1'
[listener-2] [INFO] [1726427687.714343316] [listener]: I heard: [Hello World: 1]
[talker-1] [INFO] [1726427688.712840861] [talker]: Publishing: 'Hello World: 2'
[listener-2] [INFO] [1726427688.713186962] [listener]: I heard: [Hello World: 2]
```

Aqui está a aparência desse arquivo de launch:

```python
"""Inicia um talker e um listener."""
from launch import LaunchDescription
import launch_ros.actions

def generate_launch_description():
    return LaunchDescription([
        launch_ros.actions.Node(
            package='demo_nodes_cpp',
            executable='talker',
            output='screen'),
        launch_ros.actions.Node(
            package='demo_nodes_cpp',
            executable='listener',
            output='screen'),
    ])

```

Neste arquivo, você encontrará um conjunto de módulos Python utilizados internamente. Note a função única chamada `generate_launch_description()`. Esta função é o **padrão** nos arquivos de launch do ROS 2: sempre que executamos um comando de launch, o sistema chama essa função, que deve obrigatoriamente retornar um objeto do tipo `LaunchDescription`.

A classe `LaunchDescription` funciona como um "contêiner" para o arquivo de launch, guardando informações sobre quais nós, parâmetros e configurações devem ser iniciados. Também vemos a classe `Node()`, que auxilia na execução de um nó com sua configuração específica. Os objetos `Node` são inseridos dentro do `LaunchDescription` e retornados pela função para que o ROS possa executá-los.

Discutiremos mais detalhes sobre arquivos de launch no próximo capítulo. Você também pode ler mais no link: ***[Criando um arquivo de launch](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Creating-Launch-Files.html)***.


Após discutirmos os conceitos mais importantes, vamos colocar a mão na massa com os pacotes de demonstração do ROS 2.

## Construindo um pacote ROS 2

Pacotes (**Packages**) são as unidades básicas de software no ROS 2. Eles são organizados dentro de um **ROS 2 Workspace** (espaço de trabalho), onde podemos buildar (compilar) os pacotes e executar os nós.

Criar um workspace no ROS 2 é muito simples, e você pode ter quantos desejar em seu sistema operacional. O objetivo principal do workspace é organizar um conjunto de pacotes relacionados. Por exemplo: se você estiver trabalhando em um projeto de navegação, pode manter todos os pacotes pertinentes dentro de um mesmo workspace. Essa é uma excelente prática para manter a organização dos arquivos do seu robô.

Existem dois tipos de espaços de trabalho (**workspaces**) no ROS 2. O primeiro é o **base workspace**, que se refere à própria instalação do ROS 2. Nós adicionamos o comando `source /opt/ros/<distro>/setup.bash` no arquivo `~/.bashrc` para carregar esse workspace base. Se ele não for carregado, os pacotes e ferramentas principais do ROS não ficarão visíveis no terminal.

O segundo tipo é o **overlay workspace**. Estes são os espaços de trabalho criados pelo usuário. Uma vez criados, você pode buildar (compilar) o workspace e sobrepô-lo ao workspace base, carregando o arquivo `setup.bash` localizado na pasta `install`. No ROS 2, podemos criar múltiplos workspaces e sobrepô-los uns aos outros.


### Criando um workspace no ROS 2

Um workspace do ROS 2 nada mais é do que uma pasta que contém uma subpasta chamada `src`. Abaixo, o comando para criar um workspace chamado `master_ros2_ws` na sua pasta home (o comando também cria a pasta `src` automaticamente):

```bash
mkdir -p ~/master_ros2_ws/src
```

Após criar as pastas, entre na pasta `src`. É aqui que criaremos novos pacotes ou copiaremos pacotes já existentes:

```bash
cd ~/master_ros2_ws/src
```

Quando terminar de mexer nos pacotes, volte para a pasta raiz do workspace:

```bash
cd ~/master_ros2_ws
```

Agora podemos buildar o workspace. Vale notar que você pode buildar o workspace mesmo que ele ainda não tenha nenhum pacote dentro.


### "Buildando" o Workspace
Antes de compilar, a melhor prática é usar o seguinte comando para instalar as dependências dos pacotes:

```bash
rosdep install -i --from-path src --rosdistro jazzy -y
```

O comando `rosdep` localiza as dependências dos pacotes dentro da pasta `src` e verifica se elas já estão instaladas no seu sistema operacional. Caso não estejam, ele as instala automaticamente. Este é um comando extremamente prático para gerenciar problemas de dependência no ROS 2.

Após instalar as dependências, você pode finalmente buildar o seu workspace.

Você pode utilizar o seguinte comando para compilar os pacotes dentro do seu workspace:

```bash
colcon build
```

O comando `colcon` é a ferramenta de compilação (**build tool**) comumente utilizada no ROS 2 para construir os pacotes dentro de um workspace. É necessário estar na pasta raiz do workspace do ROS 2 antes de iniciar a compilação.

Podemos compilar todos os pacotes de uma vez ou selecionar pacotes específicos:

* **`colcon build`**: Compila todos os pacotes presentes no workspace.
* **`colcon build --packages-select <nome_do_pacote>`**: Compila seletivamente apenas o pacote especificado.

Outra variação importante é o comando `colcon build --symlink-install`. O parâmetro `symlink-install` cria **links simbólicos** (symlinks) no diretório `install/` em vez de copiar os arquivos fisicamente. Esta é uma excelente opção ao trabalhar com **nós em Python**: se você modificar o código do nó Python, não precisará recompilar o pacote, pois o arquivo executável na pasta `install` já aponta diretamente para o seu arquivo de código original.

Assim que você executar o comando, verá mensagens confirmando que os pacotes foram construídos. Esse processo envolve a compilação de código-fonte, como em C++. Após o sucesso, você encontrará três pastas principais ao lado da pasta `src`:

| Pasta | Descrição |
| --- | --- |
| **build** | Onde os arquivos intermediários da compilação são armazenados. |
| **install** | Onde ficam os executáveis, scripts e arquivos de configuração prontos para uso. |
| **log** | Contém mensagens de log e histórico detalhado do processo de build. |

Você pode ler mais sobre o comando `colcon` no link oficial: [Using colcon to build packages](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Colcon-Tutorial.html).


Após compilar o workspace com sucesso, podemos adicioná-lo como um **overlay** (sobreposição) ao sistema utilizando o seguinte comando:

```bash
source ~/master_ros2_ws/install/setup.bash
```

Após carregar esse overlay, você poderá executar os nós e arquivos de launch contidos nesses pacotes. Aprenderemos mais detalhes sobre os workspaces do ROS no próximo capítulo. Você também pode consultar: ***[Creating a workspace](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.html)***.

Discutimos a maioria dos conceitos cruciais do ROS 2. Agora, vamos ver como implementar esses conceitos na prática em nosso código.
