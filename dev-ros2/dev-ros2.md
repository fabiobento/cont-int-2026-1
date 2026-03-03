# Aula 2: Escrevendo e Construindo um Nó ROS 2

Para escrever seu próprio código personalizado com o ROS 2, você terá que criar programas ROS 2 ou, em outras palavras, nós (*nodes*). Você já descobriu o conceito de nós no Capítulo 3.

Antes de criar um nó, há um pouco de configuração a fazer: você precisa criar um *workspace* (espaço de trabalho) do ROS 2, no qual construirá sua aplicação. Neste *workspace*, você adicionará pacotes para organizar melhor seus nós. Então, nesses pacotes, você poderá começar a escrever seus nós. Depois de escrever um nó, você irá compilá-lo (*build*) e executá-lo.

Faremos todo este processo em container, conforme visto na aula 1, com código prático e linhas de comando ao longo de todo o caminho. Este é o processo que você repetirá para qualquer novo nó que criar ao desenvolver uma aplicação ROS 2.

Ao final desta aula, você será capaz de criar seus próprios pacotes e nós do ROS 2 com Python e C++. Você também será capaz de executar e inspecionar seus nós pelo terminal. Este é o degrau necessário para aprender qualquer outra funcionalidade do ROS 2. Não existe tópico, serviço, ação, parâmetro ou arquivo de inicialização (*launch file*) sem nós.

Todas as explicações começarão com Python, seguidas por C++, que cobriremos mais rapidamente. Se você deseja aprender apenas com Python, pode pular as seções de C++. No entanto, se quiser aprender com C++, a leitura das explicações anteriores de Python é obrigatória para a compreensão.

## Criando e configurando um workspace do ROS 2

Antes de escrevermos qualquer código, precisamos de um pouco de organização. Os nós existirão dentro de pacotes, e todos os seus pacotes existirão dentro de um *workspace* (espaço de trabalho) do ROS 2.

O que é um workspace do ROS 2? Um workspace nada mais é do que uma organização de pastas na qual você criará e compilará seus pacotes. Toda a sua aplicação ROS 2 viverá dentro deste workspace.

Para criar um, você deve seguir certas regras. Vamos criar o seu primeiro workspace passo a passo e configurá-lo corretamente.

### Criando um workspace

Para criar um workspace, você simplesmente criará um novo diretório dentro do seu diretório pessoal (*home*).

Quanto ao nome do workspace, vamos mantê-lo simples por enquanto e usar algo que seja reconhecível: `master_ros2_ws`.

> **Observação:**
>
> O nome do workspace não é importante e não afetará nada em sua aplicação. Como estamos apenas começando, temos apenas um workspace. À medida que você progredir e começar a trabalhar em diversas aplicações, a melhor prática é nomear cada workspace com o nome da aplicação ou do robô. Por exemplo, se você criar um workspace para um robô chamado **ABC V3**, poderá nomeá-lo como `abc_v3_ws`.

Abra o terminal, e navegue para seu diretório pessoal (*home*), e crie o workspace. É aqui que você escreverá todo o código para a sua aplicação ROS 2:

```bash
$ cd
$ mkdir -p ~/master_ros2_ws/src
```
Isso é tudo o que há para fazer. Para configurar um novo *workspace*, basta criar um novo diretório (em algum lugar na sua pasta pessoal) e criar um diretório `src` dentro dele.
> **Observação Importante:**
>
> Como trabalharemos dentro de um container, o workspace será criado dentro dele. Então, antes de seguir os próximos passos, vá para o diretório `dev-ros2/scripts/docker_dev` do [repositório da disciplina](https://github.com/fabiobento/cont-int-2026-1) que você baixou e execute o script para iniciar o container:
> ```bash
    > $ ./start_container.sh ros2_dev
> ```

### Compilando o workspace

Mesmo que o workspace esteja vazio (ainda não criamos nenhum pacote), ainda assim podemos compilá-lo. Para fazer isso, siga estas etapas:

1. Navegue até o diretório raiz do workspace. Certifique-se de que você está no lugar certo.
2. Execute o comando `colcon build`. O **colcon** é o sistema de compilação do ROS 2 e foi instalado quando você instalou os pacotes `ros-dev-tools` na aula 1.

Vamos compilar o workspace:

```bash
$ cd ~/master_ros2_ws
$ colcon build
```

> **Observação Importante:**
>
> Você deve sempre executar o `colcon build` a partir da raiz do diretório do seu workspace, e não de qualquer outro lugar. Se você cometer um erro e executar este comando em outro diretório (por exemplo, dentro do diretório `src` do workspace ou dentro de um pacote), simplesmente remova os novos diretórios `install`, `build` e `log` que foram criados no lugar errado. Em seguida, volte para o diretório raiz do workspace e compile novamente.


Como você pode ver, nenhum pacote foi compilado, mas vamos listar todos os diretórios dentro de `~/master_ros2_ws`:

```bash
$ ls -F ~/master_ros2_ws
```

Você verá a listagem dos seguintes diretórios:

```bash
$ build/  install/  log/  src/
```

Após executar o comando de compilação `colcon build`, o seu workspace será organizado em quatro diretórios principais, cada um com uma função específica no ciclo de desenvolvimento:

* **`src/` (Source Space):** É o diretório onde reside o seu código-fonte. Aqui você criará seus pacotes, escreverá seus scripts Python ou arquivos C++, e definirá suas mensagens personalizadas. É a única pasta que você manipula diretamente.
* **`build/` (Build Space):** Funciona como um "espaço de rascunho" para o compilador. Nela, o `colcon` armazena arquivos temporários e configurações intermediárias geradas durante o processo de construção. Se algo der errado na compilação, apagar esta pasta costuma ser o primeiro passo para uma limpeza.
* **`install/` (Install Space):** É a pasta mais crítica para a execução. Após a compilação, todos os executáveis, scripts e recursos são organizados aqui. Quando você "ativa" o seu workspace, o ROS 2 busca os comandos e nós dentro desta pasta, e não na `src`.
* **`log/` (Log Space):** Contém registros detalhados sobre cada processo de compilação realizado. Caso o `colcon build` falhe, é aqui que você encontrará os arquivos de texto que explicam exatamente qual erro ocorreu, facilitando a depuração.

Podemos comparar com um projeto de placa de circuito impresso (PCB): a pasta **`src`** são os seus esquemáticos e o layout no software; a **`build`** são os arquivos Gerber temporários; e a **`install`** é a placa física pronta para ser populada e ligada.

### Ativando (Sourcing) o workspace

Se você navegar para dentro do diretório `install` recém-criado, poderá ver um arquivo `setup.bash`:

```bash
$ ls ~/master_ros2_ws/install
COLCON_IGNORE             _local_setup_util_sh.py  local_setup.ps1  local_setup.zsh  setup.ps1  setup.zsh
_local_setup_util_ps1.py  local_setup.bash         local_setup.sh   setup.bash       setup.sh
```

> **Observação :** Esse arquivo `setup.bash` dentro da pasta `install` é o que "avisa" ao sistema operacional onde os seus novos programas (pacotes) estão localizados. Sem rodar esse arquivo, o comando `ros2 run` não conseguirá encontrar nada do que você desenvolveu.

Isso pode parecer familiar. Confira a linha 40 do [Dockerfile](https://github.com/fabiobento/cont-int-2026-1/blob/main/fundamentos-ros2/scripts/ros2_jazzy_docker/docker_gui/Dockerfile.master_ros2) que você usou anteriormente. Se você se lembra, após instalarmos o ROS 2, nós ativamos (*sourced*) um script bash semelhante a partir do diretório de instalação do ROS 2 (`/opt/ros/jazzy/setup.bash`) para que pudéssemos usar o ROS 2 em nosso ambiente. Precisaremos fazer o mesmo para o nosso *workspace*.

Toda vez que você compilar seu *workspace*, você deve ativá-lo para que o ambiente (a sessão em que você está) saiba sobre as novas mudanças no *workspace*.

Para ativar o *workspace*, execute o script `setup.bash`:
```bash
$ source ~/master_ros2_ws/install/setup.bash
```

Então, como fizemos anteriormente, vamos adicionar essa linha ao nosso `.bashrc`. Dessa forma, você não precisará ativar (*source*) o workspace toda vez que abrir um novo terminal.

Como em ambientes de container Docker o sistema costuma ser minimalista e não possui editores de texto instalados, utilizaremos o comando `echo` para adicionar as configurações diretamente ao final do arquivo.

Isso garantirá que as configurações do ROS 2 sejam carregadas automaticamente toda vez que você abrir o terminal.

Execute o comando abaixo para adicionar a ativação da instalação global do ROS 2 e, em seguida, a do seu workspace pessoal. **Atenção:** A ordem é fundamental; o workspace deve ser carregado por último para que suas customizações tenham prioridade.

```bash
# Adicionando as configurações ao final do .bashrc
$ echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
$ echo "source ~/master_ros2_ws/install/setup.bash" >> ~/.bashrc
```
>> **Por que a ordem importa?**
>
> O ROS 2 funciona através de um sistema de "camadas" (*underlays* e *overlays*).
>
> * A instalação global em `/opt/ros/` é a base (**underlay**).
> * O seu workspace pessoal em `~/ros2_ws/` é a camada superior (**overlay**).
>
> Se você inverter a ordem, o sistema pode tentar carregar ferramentas básicas sobre as suas ferramentas personalizadas, o que causa erros de dependência ou impede que o ROS 2 reconheça as modificações que você fez nos pacotes padrão.


Após executar os comandos acima, você deve recarregar o arquivo para que as mudanças entrem em vigor imediatamente:

```bash
$ source ~/.bashrc
```

Para conferir se o texto foi inserido corretamente sem precisar de um editor, você pode usar o comando `tail`:

```bash
# Mostra as últimas 5 linhas do arquivo
$ tail -n 5 ~/.bashrc
```

> **Observação:**
>
> Se você compilar o workspace em um ambiente que já foi ativado (*sourced*), ainda assim precisará ativar o workspace mais uma vez, pois houve alterações e o ambiente não está ciente delas. Neste caso, você pode ativar o script `setup.bash` do workspace diretamente, ativar o `.bashrc` ou simplesmente abrir um novo terminal.

Seu workspace agora está configurado corretamente e você pode compilar sua aplicação. Próximo passo: criando um pacote.

## Criando um pacote

Qualquer nó que você criar existirá dentro de um pacote. Portanto, para criar um nó, primeiro você deve criar um pacote (dentro do seu *workspace*). Você aprenderá agora como criar seus próprios pacotes e veremos as diferenças entre pacotes em Python e C++.

Mas primeiro, o que exatamente é um pacote?

> **Observação**
> No ROS 2, **não se cria um script solto**. Tudo precisa estar organizado em pacotes para que o sistema de compilação (`colcon`) e o sistema de execução (`ros2 run`) consigam localizar as dependências e os executáveis.

### O que é um pacote do ROS 2?

Um pacote ROS 2 é uma subparte da sua aplicação.

Consideremos um braço robótico que queremos utilizar para pegar e colocar objetos (*pick and place*). Antes de criarmos qualquer nó, podemos tentar dividir esta aplicação em várias subpartes, ou pacotes.

Poderíamos ter um pacote para gerir uma câmera, outro pacote para o controle do hardware (motores) e ainda outro pacote para calcular o planejamento de movimento (*motion planning*) do robô.

<a id="figure-2-1"></a>

![](https://github.com/fabiobento/cont-int-2026-1/raw/main/dev-ros2/imagens/pacote-ros2.jpg)
**Figura 2-1 - Exemplo da organização de pacotes para um robô de pick and place.** ([Fonte](https://www.packtpub.com/en-us/product/ros-2-from-scratch-9781835881415))


Cada pacote é uma unidade independente, responsável por uma subparte da sua aplicação.

Os pacotes são muito úteis para organizar os seus nós e também para gerir corretamente as dependências, como veremos mais adiante neste livro.

Agora, vamos criar um pacote, e aqui você precisará fazer uma escolha. Se você quiser criar um nó com Python, criará um pacote Python; se quiser criar um nó com C++, criará um pacote C++. A arquitetura para cada tipo de pacote é bastante diferente.

> **Observação**
> * **Pacotes Python:** Utilizam o `setuptools` e são mais dinâmicos para prototipagem rápida.
> * **Pacotes C++:** Utilizam o `CMake`, exigindo uma estrutura de compilação um pouco mais rígida, mas oferecendo maior desempenho para tarefas críticas de tempo real.

### Criando um pacote Python

Você criará todos os seus pacotes no diretório `src` do seu workspace ROS 2. Portanto, certifique-se de navegar para este diretório antes de fazer qualquer outra coisa:
```bash
$ cd ~/master_ros2_ws/src
```

>> **Observação Importante**
>> Regra de "ouro":
>> * **Criar** pacotes e **escrever** código: sempre dentro da pasta **`src/`**.
>> * **Compilar** (`colcon build`): sempre na **raiz** do workspace.

Aqui está como construir o comando para criar um pacote:

* **`ros2 pkg create <nome_do_pacote>`**: Este é o mínimo que você precisa escrever.
* Você pode especificar um tipo de compilação (*build type*) com **`--build-type <tipo_de_compilação>`**. Para um pacote Python, precisamos usar **`ament_python`**.
* Você também pode especificar algumas dependências opcionais com **`--dependencies <lista_de_dependências_separadas_por_espaços>`**. É sempre possível adicionar dependências mais tarde no pacote.

Vamos criar nosso primeiro pacote chamado **`my_py_pkg`**. Usaremos este nome como um exemplo para trabalhar com os principais conceitos do ROS 2. Depois, conforme progredirmos, usaremos nomes mais significativos. No diretório `src` do seu workspace, execute o seguinte:

```bash
$ ros2 pkg create my_py_pkg --build-type ament_python --dependencies rclpy
```
> **Observação:**
> O parâmetro `--build-type ament_python` é o que diferencia um projeto Python de um C++ (que usaria `ament_cmake`). Se você esquecer essa flag, o ROS 2 tentará criar um pacote C++ por padrão, o que causará erros quando você tentar rodar scripts Python.

Com este comando, dizemos que queremos criar um pacote chamado **my_py_pkg**, com o tipo de compilação **ament_python**, e especificamos uma dependência: **rclpy** — esta é a biblioteca Python para ROS 2 que você usará em todos os seus nós Python.

Isso imprimirá vários registros (*logs*), mostrando quais arquivos foram criados. Você também pode receber um aviso de **[WARNING]** sobre a falta de uma licença, mas como não temos a intenção de publicar este pacote em lugar nenhum, não precisamos de um arquivo de licença agora. Você pode ignorar este aviso.

Você poderá ver então que existe um novo diretório chamado `my_py_pkg`. Aqui está a arquitetura do seu pacote Python recém-criado:

```bash
/home/robot/master_ros2_ws/src/my_py_pkg
├── my_py_pkg
│   └── __init__.py
├── package.xml
├── resource
│   └── my_py_pkg
├── setup.cfg
├── setup.py
└── test
    ├── test_copyright.py
    ├── test_flake8.py
    └── test_pep257.py
```

> **Observação:**
> O **rclpy** (ROS Client Library for Python) é o "coração" do desenvolvimento com Python no ROS 2. Sem adicionar essa dependência na criação do pacote (ou manualmente depois no `package.xml`), o código não conseguirá importar as funções básicas do ROS.

Dentro do diretório de seu pacote, você encontrará a seguinte estrutura:

* **`package.xml`**: Este arquivo contém informações de metadados sobre o seu pacote (nome, versão, autor, licença) e, mais importante, a lista de dependências que o pacote precisa para funcionar.
* **`setup.py`**: Um arquivo padrão do ecossistema Python. Ele contém as instruções de como instalar o seu pacote e como o ROS 2 deve encontrar os seus scripts executáveis.
* **`setup.cfg`**: Contém configurações necessárias para que o sistema saiba onde os scripts de entrada do pacote estão localizados.
* **`my_py_pkg/` (Subpasta com o mesmo nome)**: Este é o diretório principal do módulo Python. É aqui que você colocará todos os seus scripts `.py` e criará a lógica dos seus nós.
* **`resource/`**: Uma pasta usada pelo sistema de ferramentas do ROS 2 para identificar o pacote durante o processo de build.
* **`test/`**: O local destinado a testes unitários para garantir que o seu código funciona como esperado.

> **Observação:**
> Um erro comum é colocar o código diretamente na raiz da pasta `my_py_pkg`. É fundamental que o código vá para dentro da **subpasta** `my_py_pkg` (aquela que já contém um arquivo vazio chamado `__init__.py`).


### Criando um pacote C++

Trabalharemos muito com Python neste curso, mas para fins de completude, também incluirei o código em C++ para todos os exemplos. 

Criar um pacote C++ é muito semelhante a criar um pacote Python; no entanto, a arquitetura do pacote será bastante diferente.

Certifique-se de navegar até o diretório `src` do seu workspace e, em seguida, crie um novo pacote. Vamos usar um padrão semelhante ao que fizemos para o Python e nomear o pacote como `my_cpp_pkg`:

```bash
$ cd ~/master_ros2_ws/src/
$ ros2 pkg create my_cpp_pkg --build-type ament_cmake --dependencies rclcpp
```

> **Observação:**
> * **Python (`ament_python`)**: Usa o `setup.py`. É interpretado, o que facilita testes rápidos no robô sem precisar de uma compilação pesada.
> * **C++ (`ament_cmake`)**: Usa o `CMakeLists.txt`. É compilado, o que oferece uma performance superior para tarefas que exigem processamento intenso ou tempo real, mas a estrutura de pastas é mais rígida (com pastas separadas para `include` e `src`).

Escolhemos **`ament_cmake`** para o tipo de compilação (o que significa que este será um pacote C++) e especificamos uma dependência: **`rclcpp`** — esta é a biblioteca C++ para o ROS 2, que usaremos em todos os nossos nós C++.

Mais uma vez, você verá vários registros (*logs*) com os arquivos recém-criados e, talvez, um aviso sobre a licença que você pode ignorar.

A arquitetura do seu novo pacote C++ será assim:

```bash
/home/robot/ros2_ws/src/my_cpp_pkg/
├── CMakeLists.txt
├── include
│   └── my_cpp_pkg
├── package.xml
└── src
```

Aqui está uma explicação rápida do papel de cada arquivo ou diretório:

* **`CMakeLists.txt`**: Será usado para fornecer instruções sobre como compilar seus nós C++, criar bibliotecas e assim por diante.
* **Diretório `include`**: Em um projeto C++, você pode dividir seu código em arquivos de implementação (extensão `.cpp`) e arquivos de cabeçalho (extensão `.hpp`). Se você dividir seus nós C++ em arquivos `.cpp` e `.hpp`, deverá colocar os arquivos de cabeçalho dentro do diretório `include`.
* **`package.xml`**: Este arquivo é obrigatório para qualquer tipo de pacote ROS 2. Ele contém mais informações sobre o pacote e as dependências de outros pacotes.
* **Diretório `src`**: É aqui que você escreverá seus nós C++ (arquivos `.cpp`).

### **Compilando um pacote**

Agora que você criou um ou mais pacotes, você pode compilá-los, mesmo que ainda não tenha nenhum nó dentro deles.

Para compilar os pacotes, volte para a raiz do seu workspace ROS 2 e execute o comando `colcon build`. Mais uma vez, e como visto anteriormente neste capítulo, o local onde você executa este comando é **muito importante**.

```bash
$ cd ~/master_ros2_ws
$ colcon build
```
A saída será algo como:

```bash
Starting >>> my_cpp_pkg
Starting >>> my_py_pkg
Finished <<< my_py_pkg [1.60s]
Finished <<< my_cpp_pkg [3.46s]
Summary: 2 packages finished [3.72s]
```

Ambos os pacotes foram compilados. Você terá que fazer isso toda vez que adicionar ou modificar um nó dentro de um pacote.

O ponto importante a notar é esta linha: `Finished <<< <nome_do_pacote> [tempo]`. Isso significa que o pacote foi compilado corretamente. Mesmo que você veja registros de avisos (*warnings*) adicionais, se também vir a linha `Finished`, saberá que o pacote foi compilado.

Após compilar qualquer pacote, você também deve ativar (*source*) o seu *workspace* para que o ambiente esteja ciente das novas mudanças. Você pode fazer qualquer **uma** das seguintes opções:

* Abrir um novo terminal, já que tudo está configurado no arquivo `.bashrc`
* Ativar o script `setup.bash` diretamente (`source ~/ros2_ws/install/setup.bash`)
* Ativar o `.bashrc` manualmente (`source ~/.bashrc`)

> **Dica Importante:**
>
> Como estamos trabalhando dentro de um container, a opção de **"abrir um novo terminal"** pode não ser tão direta quanto no desktop (exigiria um novo `docker exec`).
>
> Por isso, para a dinâmica das aulas, recomendo o uso do comando:
>
> ```bash
> source ~/.bashrc
> ```
>
> Isso é mais rápido e garante que todas as alterações feitas via `echo` (como fizemos anteriormente para compensar a falta de editor de texto) sejam aplicadas instantaneamente na sessão atual do container.


Para compilar apenas um pacote específico, você pode usar a opção `--packages-select`, seguida pelo nome do pacote. Aqui está um exemplo:

```bash
$ colcon build --packages-select my_py_pkg
Starting >>> my_py_pkg
Finished <<< my_py_pkg [1.01s]
Summary: 1 package finished [1.26s]
```


> **Observação:**
> Quando estiver trabalhando no **Raspberry Pi** ou em containers com muitos pacotes, usar o comando `colcon build --packages-select <nome_do_pacote>` é uma ótima estratégia para:
> * **Economia de tempo:** Conforme o projeto cresce, rodar apenas `colcon build` vai tentar compilar tudo o que estiver na pasta `src`. Se o aluno mudou apenas um script Python no `my_py_pkg`, não faz sentido o computador perder tempo verificando o pacote C++.
> * **Foco no erro:** Se um pacote específico está com erro de compilação, usar o `--packages-select` ajuda a limpar a saída do terminal, mostrando apenas os logs que interessam para aquele problema.

Agora que você compilou e ativou o seu *workspace*, você pode verificar se o ROS 2 consegue encontrar os seus pacotes. Para fazer isso, utilize o comando `ros2 pkg list`:

```bash
ros2 pkg list
```

Este comando listará todos os pacotes instalados no seu sistema (tanto os globais do ROS 2 quanto os seus). Como a lista será bem grande, você pode usar o comando `grep` para filtrar e encontrar especificamente os seus pacotes:

```bash
ros2 pkg list | grep my_

```
Se tudo estiver correto, você deverá ver os nomes `my_py_pkg` e `my_cpp_pkg` no terminal.


Agora que criamos alguns pacotes e sabemos como compilá-los, podemos criar nós dentro deles. Mas como vamos organizá-los?

### Como os nós são organizados em um pacote?

Para desenvolver uma aplicação ROS 2, você escreverá código dentro de nós (*nodes*). Um nó é simplesmente o nome de um programa ROS 2.

Um nó é um subprograma da sua aplicação, responsável por uma única coisa. Se você tiver duas funcionalidades diferentes para implementar, então terá dois nós. Os nós se comunicam entre si usando as comunicações do ROS 2 (tópicos, serviços e ações).

Você organizará seus nós dentro de pacotes. Para um único pacote (subparte da sua aplicação), você pode ter vários nós (funcionalidades). Para entender completamente como organizar pacotes e nós, você precisará de prática e experiência. Por enquanto, vamos apenas ter uma ideia com um exemplo.

Vamos voltar à arquitetura de pacotes que tínhamos na [Figura 2-1](#figure-2-1)  e adicionar nós dentro dos pacotes:

<a id="figure-2-2"></a>

![](https://github.com/fabiobento/cont-int-2026-1/raw/main/dev-ros2/imagens/pacote-org-ros2.jpg)
**Figura 2-2 - Exemplo da organização de pacotes para um pacote em nós.** ([Fonte](https://www.packtpub.com/en-us/product/ros-2-from-scratch-9781835881415))

