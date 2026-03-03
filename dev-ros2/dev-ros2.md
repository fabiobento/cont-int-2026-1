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
cd
mkdir -p ~/master_ros2_ws/src
```
Isso é tudo o que há para fazer. Para configurar um novo *workspace*, basta criar um novo diretório (em algum lugar na sua pasta pessoal) e criar um diretório `src` dentro dele.
> **Observação Importante:**
>
> Como trabalharemos dentro de um container, o workspace será criado dentro dele. Então, antes de seguir os próximos passos, vá para o diretório `dev-ros2/scripts/docker_dev` do [repositório da disciplina](https://github.com/fabiobento/cont-int-2026-1) que você baixou e execute o script para iniciar o container:
> ```bash
    > ./start_container.sh ros2_dev
> ```

### Compilando o workspace

Mesmo que o workspace esteja vazio (ainda não criamos nenhum pacote), ainda assim podemos compilá-lo. Para fazer isso, siga estas etapas:

1. Navegue até o diretório raiz do workspace. Certifique-se de que você está no lugar certo.
2. Execute o comando `colcon build`. O **colcon** é o sistema de compilação do ROS 2 e foi instalado quando você instalou os pacotes `ros-dev-tools` na aula 1.

Vamos compilar o workspace:

```bash
cd ~/master_ros2_ws
colcon build
```

> **Observação Importante:**
>
> Você deve sempre executar o `colcon build` a partir da raiz do diretório do seu workspace, e não de qualquer outro lugar. Se você cometer um erro e executar este comando em outro diretório (por exemplo, dentro do diretório `src` do workspace ou dentro de um pacote), simplesmente remova os novos diretórios `install`, `build` e `log` que foram criados no lugar errado. Em seguida, volte para o diretório raiz do workspace e compile novamente.


Como você pode ver, nenhum pacote foi compilado, mas vamos listar todos os diretórios dentro de `~/master_ros2_ws`:

```bash
ls -F ~/master_ros2_ws
```

Você verá a listagem dos seguintes diretórios:

```bash
build/  install/  log/  src/
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
ls ~/master_ros2_ws/install
COLCON_IGNORE             _local_setup_util_sh.py  local_setup.ps1  local_setup.zsh  setup.ps1  setup.zsh
_local_setup_util_ps1.py  local_setup.bash         local_setup.sh   setup.bash       setup.sh
```

> **Observação :** Esse arquivo `setup.bash` dentro da pasta `install` é o que "avisa" ao sistema operacional onde os seus novos programas (pacotes) estão localizados. Sem rodar esse arquivo, o comando `ros2 run` não conseguirá encontrar nada do que você desenvolveu.

Isso pode parecer familiar. Confira a linha 40 do [Dockerfile](https://github.com/fabiobento/cont-int-2026-1/blob/main/fundamentos-ros2/scripts/ros2_jazzy_docker/docker_gui/Dockerfile.master_ros2) que você usou anteriormente. Se você se lembra, após instalarmos o ROS 2, nós ativamos (*sourced*) um script bash semelhante a partir do diretório de instalação do ROS 2 (`/opt/ros/jazzy/setup.bash`) para que pudéssemos usar o ROS 2 em nosso ambiente. Precisaremos fazer o mesmo para o nosso *workspace*.

Toda vez que você compilar seu *workspace*, você deve ativá-lo para que o ambiente (a sessão em que você está) saiba sobre as novas mudanças no *workspace*.

Para ativar o *workspace*, execute o script `setup.bash`:
```bash
source ~/master_ros2_ws/install/setup.bash
```

Então, como fizemos anteriormente, vamos adicionar essa linha ao nosso `.bashrc`. Dessa forma, você não precisará ativar (*source*) o workspace toda vez que abrir um novo terminal.

Como em ambientes de container Docker o sistema costuma ser minimalista e não possui editores de texto instalados, utilizaremos o comando `echo` para adicionar as configurações diretamente ao final do arquivo.

Isso garantirá que as configurações do ROS 2 sejam carregadas automaticamente toda vez que você abrir o terminal.

Execute o comando abaixo para adicionar a ativação da instalação global do ROS 2 e, em seguida, a do seu workspace pessoal. **Atenção:** A ordem é fundamental; o workspace deve ser carregado por último para que suas customizações tenham prioridade.

```bash
# Adicionando as configurações ao final do .bashrc
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
echo "source ~/master_ros2_ws/install/setup.bash" >> ~/.bashrc
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
source ~/.bashrc
```

Para conferir se o texto foi inserido corretamente sem precisar de um editor, você pode usar o comando `tail`:

```bash
# Mostra as últimas 5 linhas do arquivo
tail -n 5 ~/.bashrc
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

![alt text](imagens/pacotes_ros2.png)
