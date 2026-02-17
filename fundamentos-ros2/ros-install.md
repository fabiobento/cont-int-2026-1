# Aula 1: Primeiros Passos com ROS 2

Na aula incial:

- Definimos um fluxo de desenvolvimento de um robô autônomo que integra Percepção, Decisão e Ação.

- Apresentamos o stack tecnológico industrial do curso, posicionando o ROS 2 como o "sistema nervoso" central para conectividade,

- o Python com PyTorch como o "cérebro" para processamento de IA, e

- o Gazebo como o ambiente de validação física.

- Definimos um roteiro semestral que evoluirá da infraestrutura básica e visão computacional para a otimização com sistemas Fuzzy e Evolutivos, evoluindo para a autonomia via Aprendizado por Reforço para o desafio final do "Robô Navegador Inteligente"


Na aula de hoje você terá uma visão prática de como configurar rapidamente o ROS 2 no Ubuntu 24.04 em qualquer computador e começar a trabalhar com ele.
- Exploraremos algumas maneiras de instalar o ROS 2 em nossos computadores.
- Após a configuração, começaremos a nos familiarizar com o básico.
- Em seguida, discutiremos os conceitos do ROS 2 usando suas ferramentas, pacotes, workspace e o Turtlesim — um simulador 2D que pode ser usado para aprender os conceitos do framework.
- Por fim, veremos uma discussão detalhada sobre as bibliotecas de cliente (client libraries) do ROS 2, que ajudam os desenvolvedores a escrever aplicações baseadas em ROS 2 em múltiplas linguagens de programação.
- Depois de compreender as bibliotecas de cliente, aprenderemos como começar a desenvolver software para robôs usando o ROS 2.

## Requisitos Técnicos 

Para acompanhar este roteiro, é recomendável ter um computador ou placa embarcada (por exemplo, Raspberry Pi, placa Jetson, etc.) com o Ubuntu 24.04 LTS instalado ou qualquer outra versão do Ubuntu.

Os materiais de referência para este roteiro podem ser encontrados na pasta `fundamentos-ros2` do seguinte repositório no GitHub: https://github.com/fabiobento/cont-int-2026-1/tree/main/fundamentos-ros2.

## Instalação do ROS 2

Os computadores da maioria dos robôs rodam uma distribuição **Linux**, sendo o **Ubuntu** a mais comum. O computador a ser escolhido para o robô depende dos requisitos da aplicação robótica; podem ser PCs industriais com arquitetura x86_64 ou módulos de computação baseados em ARM64, como o Jetson Orin ou o Raspberry Pi.

Como você sabe, faremos o **deploy (implantação)** da aplicação no **computador do robô**.
- No entanto, o desenvolvimento do software de robótica ocorrerá, na maioria das vezes, em uma estação de trabalho ou laptop de desenvolvedor, que pode estar equipado com Windows, Ubuntu ou macOS.
- Então o ROS 2 pode ser instalado em todas as plataformas?
    - Sim. Isso é possível com a ajuda de ferramentas como Docker, VirtualBox, VMware, UTM e assim por diante.
- Vamos explorar diferentes maneiras de instalar o ROS 2 em um robô e em nossa máquina de desenvolvimento.

### Instalando o Ubuntu 24.04 LTS e o ROS 2 Jazzy

Este curso foca principalmente no ROS 2 Jazzy, que é compatível prioritarmente com o [Ubuntu 24.04 LTS](https://ubuntu.com/download/desktop) (LTS significa Long-Term Support ou Suporte de Longo Prazo). O ROS 2 Jazzy não será instalado em nenhuma outra versão do Ubuntu além da 24.04. Então, vamos explorar como configurar o Ubuntu 24.04 em nossa máquina de desenvolvimento e no robô.

#### Instalando o Ubuntu 24.04 LTS

Existem várias maneiras de configurar o Ubuntu 24.04 em um computador. Aqui estão algumas referências para começar a instalação do Ubuntu 24.04 para configurar o ROS 2 Jazzy:

- **Configurando o Ubuntu na estação de trabalho de desenvolvimento (arquitetura x86_64/ARM64):**
    - **Instalação do Ubuntu em dual boot**:
    Suponha que você tenha uma estação de trabalho de desenvolvimento com um processador Intel ou AMD com arquitetura baseada em x86_64. Nesse caso, você pode baixar a imagem ISO oficial no site do Ubuntu, gravá-la em um pendrive e instalá-la em sua máquina real com Windows ou outro SO. Se você já tem outro sistema operacional, como o Windows, em sua máquina, pode fazer uma instalação em dual-boot seguindo [estas instruções 2](https://ubuntuhandbook.org/index.php/2024/04/install-ubuntu-24-04-desktop/). Certifique-se de optar pela instalação manual conforme as instruções. A instalação manual nos permitirá formatar a partição desejada na unidade de disco. Instalar o Ubuntu em uma máquina real terá um desempenho melhor do que qualquer outro método de virtualização, pois funciona sem outras camadas de software.
    - **Instalando o Ubuntu no VirtualBox/VMware/WSL 2**:
    Instalar o Ubuntu em uma máquina real às vezes é arriscado para iniciantes. Devido a erros, o SO pode ocasionalmente travar e não inicializar depois disso. Se você se sente confortável trabalhando com outro SO, como Windows 10/11 ou macOS, pode instalar o Ubuntu virtualmente nesses sistemas operacionais. Softwares como **VirtualBox** e **VMware** podem ser instalados nesses sistemas, e o Ubuntu pode ser instalado usando-os. Esses tipos de programas são chamados de softwares de virtualização. Você pode baixar o [VirtualBox](https://www.virtualbox.org/wiki/Downloads) e o [VMware](https://www.vmware.com/products/desktop-hypervisor). O VirtualBox é gratuito para baixar e usar, e o VMware Workstation é gratuito para uso pessoal, mas não para aplicações comerciais. As instruções detalhadas sobre a instalação do Ubuntu 24.04 no VirtualBox podem ser encontradas [nesse tutorial](https://itslinuxguide.com/install-ubuntu-virtualbox/), e as instruções detalhadas para configurar o Ubuntu 24.04 no VMware podem ser encontradas [nesse vídeo](https://youtu.be/SgfrHKg81Qc).
    O Windows 10/11 vem com o **Windows Subsystem for Linux (WSL)**, um recurso adicional do Windows que permite aos desenvolvedores executar ambientes Linux, como o Ubuntu, sem a necessidade de máquinas virtuais separadas. Aqui está a [referência para configurar o Ubuntu 24.04 LTS no Windows WSL 2](https://www.linuxbuzz.com/how-to-install-ubuntu-on-wsl/). O WSL 2 é uma boa opção para aprender e experimentar o Ubuntu sem precisar de uma configuração de dual-boot.

    - **Instalando o Ubuntu no Docker**:
    O [Docker](https://www.docker.com/) é uma plataforma de virtualização em nível de sistema operacional. A principal diferença entre softwares de virtualização, como o VirtualBox, e o Docker é que as VMs (Máquinas Virtuais) virtualizam um SO completo. Em contraste, os containers Docker virtualizam a camada de aplicação sobre o SO hospedeiro (host). Ele utiliza o conceito de conteinerização, que pode isolar a aplicação e suas dependências em unidades portáteis e leves chamadas containers. Os containers compartilham o kernel do SO hospedeiro. Precisamos de um SO host, como Ubuntu, Windows ou macOS, para instalar o Docker.

        > O Docker é comparativamente leve e ideal para a implantação (*deployment*) de aplicações ROS 2 em robôs. Muitas imagens Docker estão hospedadas publicamente no [Docker Hub](https://hub.docker.com/). Imagens Docker são arquivos que contêm todas as bibliotecas e dependências, e os containers são as instâncias em execução de uma imagem. Usando a CLI (interface de linha de comando) do Docker, podemos baixar, gerenciar e executar diferentes imagens Docker.

    Na próxima seção discutiremos a configuração do Docker, pois esta é uma tecnologia útil para implantar aplicações robóticas baseadas em ROS 2.

- **Configurando o Ubuntu no seu robô:** A maioria dos robôs possui placas baseadas em x86_64 ou ARM64, como Raspberry Pi, Jetson Orin ou um PC industrial com processador Intel ou AMD. Podemos instalar o Ubuntu nessas máquinas. Se tivermos uma máquina x86_64, o procedimento de instalação é direto; você pode seguir as instruções mencionadas anteriormente. No entanto, se tivermos placas embarcadas, como as das séries Raspberry Pi ou Jetson, as instruções são diferentes. O Ubuntu é customizado para essas placas, e podemos consultar algumas referências para instalar o Ubuntu nelas. As instruções de configuração para o Ubuntu 24.04 no Raspberry Pi 5 podem ser encontradas [nesse link](https://raspberrytips.com/install-ubuntu-desktop-raspberry-pi/), e você pode encontrar uma referência para a instalação do Ubuntu em placas Jetson [aqui](https://ubuntu.com/download/nvidia-jetson).


#### **Instalando o ROS 2 Jazzy no Ubuntu 24.04 LTS**

Esta seção fornece instruções para a instalação do ROS 2 Jazzy no Ubuntu 24.04 LTS. Estas instruções funcionarão em máquinas `x86_64` e `ARM64`.

Para facilitar a instalação, usaremos um script de shell para automatizar este procedimento de instalação e desinstalação. Você pode encontrar o script [`ros2_install_jazzy.sh`](https://raw.githubusercontent.com/fabiobento/cont-int-2026-1/main/fundamentos-ros2/scripts/ros2_install_jazzy.sh) na pasta `fundamentos-ros2/scripts/` para instalar o ROS 2 Jazzy, e o [`ros2_uninstall_jazzy.sh`](https://raw.githubusercontent.com/fabiobento/cont-int-2026-1/refs/heads/main/fundamentos-ros2/scripts/ros2_uninstall_jazzy.sh) para desinstalar o mesmo.

Você pode executar os seguintes comandos dentro da pasta `fundamentos-ros2` para instalar o ROS 2 Jazzy com um script de shell automatizado:

```bash
chmod +x ros2_install_jazzy.sh
./ros2_install_jazzy.sh
```

Para desinstalar o ROS 2 Jazzy no futuro, use este comando:

```bash
chmod +x ros2_uninstall_jazzy.sh
./ros2_uninstall_jazzy.sh
```

O script `ros2_install_jazzy.sh` automatiza a instalação completa do ROS 2 Jazzy no Ubuntu 24.04 LTS. Ele foi projetado para ser robusto, verificando dependências e configurando o ambiente de desenvolvimento tanto para Python quanto para C++.

Aqui está o resumo das etapas que ele executa:

1. Validação do Sistema: Verifica se o sistema operacional é exatamente o Ubuntu 24.04. Caso contrário, o script é encerrado para evitar instalações quebradas.
2. Configuração de `Locale` (Idioma): Configura o suporte a UTF-8 e gera as definições de idioma para pt-BR, garantindo que caracteres especiais e acentuação funcionem corretamente no terminal e nos scripts.
3. Preparação de Repositórios e Chaves: Adiciona o repositório `universe` do Ubuntu, baixa as chaves GPG oficiais da Open Robotics e configura as fontes do APT para permitir o download dos pacotes do ROS 2.
4. Escolha da Instalação: Oferece ao usuário duas opções:
    - `Desktop Full`: (Padrão) Instala tudo, incluindo simuladores e ferramentas gráficas (Rviz, Gazebo).
    - `ROS-Base`: Instala apenas o essencial (comunicação, bibliotecas básicas), ideal para robôs embarcados como suas Raspberry Pi.
5. Instalação de Ferramentas de Desenvolvimento: Além do ROS, ele instala o build-essential (`g++`, `make`), `cmake` e `ros-dev-tools`, preparando o ambiente para compilar pacotes.
6. Configuração do Ambiente (`~/.bashrc`): Adiciona automaticamente o comando `source` ao arquivo de inicialização do seu terminal, para que o ROS 2 esteja pronto para uso toda vez que você abrir o terminal. Ele também força o Python a utilizar UTF-8 globalmente.
7. Teste de Sanidade: Ao final, o script realiza três testes rápidos: verifica a variável de ambiente do ROS, testa a codificação do Python e tenta compilar um pequeno código C++ em tempo real para garantir que o compilador está funcional.

Agora que concluímos todas as etapas da instalação do ROS 2 Jazzy no Ubuntu 24.04, podemos realizar um teste para garantir que o ambiente ROS 2 esteja configurado corretamente:

1. Abra o terminal no Ubuntu e adicione mais uma aba (ou abra um novo terminal).
2. Na primeira aba, execute este comando:

    ```bash
    ros2 run demo_nodes_cpp talker
    ```

3. Na segunda aba, execute este comando:

    ```bash
    ros2 run demo_nodes_py listener
    ```

4. Se tudo estiver correto, você verá a seguinte saída:

```bash
[INFO] [1678886400.123456789] [talker]: Publishing: 'Hello World: 1'
[INFO] [1678886400.234567890] [talker]: Publishing: 'Hello World: 2'
[INFO] [1678886400.345678901] [talker]: Publishing: 'Hello World: 3'
```

5. Na segunda aba, você verá a seguinte saída:

```bash
[INFO] [1678886400.123456789] [listener]: I heard: 'Hello World: 1'
[INFO] [1678886400.234567890] [listener]: I heard: 'Hello World: 2'
[INFO] [1678886400.345678901] [listener]: I heard: 'Hello World: 3'
```

O exemplo acima é simplesmente uma demonstração de publicador/assinante (*publisher*/*subscriber*) usando o ROS 2. Se estiver funcionando corretamente, significa que a instalação e a configuração estão operacionais. Se não estiver funcionando ou se você estiver recebendo erros, certifique-se de que o carregamento das variáveis de ambiente (`source`) do ROS 2 está correto. Você pode pressionar `Ctrl + C` para encerrar cada um dos nós em execução.


### **Instalando o ROS 2 Jazzy no Windows 11/10**

Podemos instalar o ROS 2 Jazzy no Windows de várias maneiras. Aqui estão os principais métodos que podemos seguir:

* **Instalando o ROS 2 Jazzy no VirtualBox/VMware:** Já discutimos a instalação do Ubuntu 24.04 LTS em softwares de virtualização como o VirtualBox. Para instalar o ROS 2 Jazzy nele, podemos seguir as mesmas instruções discutidas para o Ubuntu 24.04 LTS. Este método é muito fácil de configurar e também seguro para experimentar o ROS 2. Mesmo que o SO convidado (*guest*) trave, isso não afetará o SO hospedeiro (*host*) principal, que aqui é o Windows.
* **Instalando o ROS 2 Jazzy no WSL 2:** O WSL é um recurso do Windows 10/11 que permite a execução de um ambiente Linux em uma máquina Windows sem a necessidade de uma máquina virtual ou configuração de dual-boot. [Aqui está o tutorial oficial sobre como habilitar o WSL no Windows](https://ubuntu.com/desktop/wsl). A primeira versão foi o WSL 1, e a mais recente é o WSL 2. O WSL 2 possui mais recursos que o WSL 1. Usando o WSL 2, podemos instalar novas versões do Ubuntu, como o Ubuntu 24.04 e 22.04. As mesmas instruções de instalação do ROS 2 Jazzy no Ubuntu 24.04 LTS podem ser seguidas para instalar o ROS 2 Jazzy no WSL 2. Ele não é baseado apenas em linha de comando, mas também pode visualizar ferramentas de interface gráfica (GUI). Também há um compartilhamento de arquivos facilitado entre o Windows e o WSL 2.
* **Instalando o ROS 2 Jazzy no Windows 10 (sem virtualização):** Podemos instalar o ROS 2 Jazzy nativamente no Windows 10, mas não no Windows 11. Este método não utiliza o WSL; tudo roda nativamente, sem camadas adicionais. As instruções de configuração são tediosas e demoradas, mas se realmente precisarmos integrar o ROS 2 com qualquer aplicação nativa de Windows, este é o caminho a seguir. [Aqui está a referência para instalar nativamente o ROS 2 Jazzy no Windows 10](https://docs.ros.org/en/jazzy/Installation/Windows-Install-Binary.html).
    > **Observação Técnica:**
    >
    > A instalação nativa no Windows costuma ser evitada na comunidade acadêmica e de pesquisa justamente pela complexidade de gerenciar dependências e a falta de suporte para muitos pacotes que são desenvolvidos especificamente para Linux. O **WSL 2** tem se tornado o padrão *de facto* para quem não pode abrir mão do Windows.

### **Instalando o ROS 2 Jazzy no Docker**

O [Docker](https://www.docker.com/) é uma tecnologia de código aberto que ajuda desenvolvedores de software a desenvolver e implantar rapidamente aplicações em Windows, Linux e macOS. O Docker também é amplamente utilizado no desenvolvimento e implantação de softwares de robótica. A principal vantagem de usar o Docker é que podemos desenvolver e implantar rapidamente sua aplicação baseada em ROS em qualquer distribuição de ROS e de Linux. Mesmo que o seu SO hospedeiro seja o Ubuntu 20.04, você pode desenvolver aplicações ROS 2 no ROS 2 Jazzy (que utiliza o Ubuntu 24.04) usando o Docker. Isso ajudará a construir e testar sua aplicação ROS 2 em diferentes distribuições de ROS 2. O único requisito é instalar o software Docker nesses sistemas operacionais. O Docker é uma tecnologia importante que utilizamos neste curso. Discutiremos o Docker em mais detalhes nesta seção.

O Docker é uma ferramenta de software para criar, implantar e executar aplicações usando uma tecnologia chamada containers. Cada container no Docker possui uma instância leve do ambiente de software para executar nossa aplicação. Esse ambiente contém código, bibliotecas e dependências, o que ajuda os containers a funcionarem em diferentes ambientes. Diferente da VM que vimos anteriormente, cada container não possui um SO separado. Os containers trabalham ao lado do kernel Linux do hospedeiro e criam uma abstração para executar diferentes ambientes. Portanto, ao contrário de uma VM, não precisamos instalar um SO completo para executar uma aplicação.

Antes de mergulharmos no Docker, vamos ver como instalá-lo no Ubuntu 24.04 LTS como máquina hospedeira. [A instalação oficial do Docker está em seu site](https://docs.docker.com/engine/install/ubuntu/). Neste curso, adicionei um script automático para realizar o mesmo procedimento. Ele instalará o Docker no Ubuntu 24.04, bem como o [**NVIDIA Container Toolkit**](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/index.html). O NVIDIA Container Toolkit permite aos usuários construir e executar containers acelerados por GPU que funcionarão em conjunto com o Docker.

#### **Instalando o Docker e o NVIDIA Container Toolkit**

Siga estes passos para instalar o Docker e o NVIDIA Container Toolkit:

1. Abra o repositório do GitHub do curso e navegue até `fundamentos-ros2/scripts/ros2_jazzy_docker/docker_setup_scripts`. Você encontrará o arquivo [`setup_docker_ubuntu.sh`](https://raw.githubusercontent.com/fabiobento/cont-int-2026-1/refs/heads/main/fundamentos-ros2/scripts/ros2_jazzy_docker/docker_setup_scripts/setup_docker_ubuntu.sh) lá. Você pode executar este script abrindo um terminal dentro desta pasta:

    ```bash
    chmod +x setup_docker_ubuntu.sh
    ./setup_docker_ubuntu.sh
    ```

Este script ajuda a instalar todas as dependências do Docker. Se você tiver uma placa de vídeo NVIDIA e o driver instalado corretamente, ele instalará o NVIDIA Container Toolkit, que fornece aceleração gráfica ao container.

2. Se tudo for instalado corretamente, você poderá verificar se o Docker está rodando em segundo plano usando o seguinte comando:

    ```bash
    systemctl status docker
    ```

    Você obterá a seguinte saída se tudo estiver configurado adequadamente:

    ![](https://github.com/fabiobento/cont-int-2026-1/raw/main/fundamentos-ros2/imagens/docker-status-check.png)


3. Se o status do Docker estiver como ativo (`active`), você poderá testar o comando `docker` no terminal para garantir que tudo esteja em ordem:
    
    ```bash
    docker info
    ```

    Você obterá a seguinte saída. Estes são todos os detalhes do sistema do Docker:

    ![](https://github.com/fabiobento/cont-int-2026-1/raw/main/fundamentos-ros2/imagens/docker-info.png)

#### **Executando o Docker com ROS 2 Jazzy**

Devemos realizar alguns passos antes de começar a trabalhar com o ROS 2 Jazzy no Ubuntu 24.04 LTS. As etapas são detalhadas nas subseções a seguir.

##### **Passo 1: Baixando (*pulling*) a imagem base e construindo uma imagem Docker personalizada**

O primeiro passo para começar a usar o Docker é baixar uma imagem base do Docker Hub ou de outra fonte. Vamos primeiro entender o que são o Docker e as imagens base.

As **imagens Docker** são arquivos que contêm todo o código da aplicação, dependências e ambiente de execução. Podemos dizer que as imagens Docker são modelos (*templates*) para criar um **container Docker**. Uma **imagem base** é a imagem inicial que utilizamos para construir nossa própria imagem Docker. Por exemplo, podemos usar a **imagem Docker do ROS 2 Jazzy** como imagem base e, a partir dela, criar a sua imagem com todas as dependências necessárias.

O [Docker Hub](https://hub.docker.com/) oferece aos desenvolvedores acesso gratuito a imagens Docker públicas e permite que eles enviem suas próprias imagens. Essas imagens permitem que os desenvolvedores as utilizem como base para criar seus containers.

Após instalar o Docker em sua máquina, você pode baixar (*pull*) diretamente a imagem Docker do ROS 2 Jazzy do Docker Hub. A [Open Robotics publica todas as imagens Docker do ROS 1 e 2 em sua conta](https://hub.docker.com/r/osrf/ros/tags). Você pode baixar qualquer imagem da conta deles.

O comando a seguir ajuda a baixar a imagem base do Jazzy do Docker Hub. Isso o levará diretamente para o ambiente do ROS 2 Jazzy sem a necessidade de instalar mais nada:

```bash
docker pull osrf/ros:jazzy-desktop-full
```

Após inserir este comando, você verá que a imagem está sendo baixada, o que levará algum tempo dependendo da velocidade da sua internet. Assim que o download terminar, você terá a imagem base do ROS 2 Jazzy. O próximo passo é criar um container usando essa imagem. Como já discutimos, as imagens Docker são como modelos (*templates*) para o container; portanto, assim que um container for iniciado, teremos o ambiente do ROS 2 Jazzy dentro dele. Trabalharemos na maior parte do tempo dentro do container usando um shell, pois a maioria das imagens base possui um ambiente leve, que não inclui um ambiente de desktop (interface gráfica) como o que vemos no Ubuntu 24.04 LTS.

Depois de obter a imagem Docker do Jazzy, podemos começar a criar um container a partir dela. A seção seguinte discute os passos necessários.

##### **Passo 2: Criando um container a partir da imagem do ROS 2 Jazzy**

Para criar um container, você pode usar o seguinte comando:
```bash
docker run -it --name cont-int-2026-1 osrf/ros:jazzy-desktop-full bash
```

Após executar este comando no seu terminal, você poderá ver um novo terminal com um usuário diferente, que pode ser o usuário root, como no exemplo abaixo:

```bash
root@eafa922c9072:/#
```

Esta linha é o shell do container ROS 2 Jazzy com o nome **master_ros2**. Se você observar o comando acima, verá que usamos o comando `docker run` para criar um container. Devemos adicionar o nome da imagem; também podemos especificar o nome do container usando o argumento `--name`.

O argumento `-it` no Docker ajuda a interagir com o container, permitindo o envio de comandos de texto através do shell **bash**. O comando `bash` ao final informa ao container Docker para executar o interpretador de comandos bash assim que ele iniciar. Portanto, este comando cria um container Docker com um shell bash interativo e o nome de **master_ros2**. O nome do container é opcional aqui; se você não incluir um nome, ele atribuirá um aleatoriamente. É melhor definir um nome para que possamos iniciar, parar e deletar este container facilmente.

Após criar o container a partir da imagem, você terá um ambiente ROS 2 Jazzy onde poderá fazer qualquer coisa. Seu progresso será perdido se você deletar o container. As alterações feitas dentro do container ficam em cache, portanto, você pode iniciar e parar o container sem perder dados. Somente a reconstrução (*rebuilding*) dele fará com que você perca quaisquer dados que não estejam montados no sistema hospedeiro (host).

Você pode realizar o seguinte teste para garantir que o ROS 2 Jazzy está funcionando corretamente.

Execute o nó publicador de exemplo no ROS 2, que publica uma string "Hello World". Isso deve ser executado no terminal do Docker:

```bash
ros2 run demo_nodes_cpp talker
```

Você obterá a seguinte saída:

```bash
[INFO] [1708036800.123456789] [talker]: Publishing: "Hello World: 1"
[INFO] [1708036801.123456789] [talker]: Publishing: "Hello World: 2"
[INFO] [1708036802.123456789] [talker]: Publishing: "Hello World: 3"
```
 Agora podemos executar um comando para se inscrever no tópico "topic" e receber as mensagens publicadas pelo nó "talker". Para rodar esse próximo comando siga apra a próxima seção

##### **Passo 3: Executando um novo comando no container ROS 2 Jazzy**

Após criar um container e acessar o shell, executamos o programa publicador (*publisher*) no ROS 2 e podemos ver que ele está funcionando.

Agora, como acessar outro terminal deste container e executar o código assinante (*subscriber*)? É aí que entram os comandos `docker exec`. Os comandos `docker exec` nos ajudam a rodar outro programa ou comando no mesmo container. Portanto, abra um novo terminal no seu SO hospedeiro e execute o seguinte comando para obter acesso ao terminal do container:

```bash
docker exec -it cont-int-2026-1 bash
```
Após carregar este comando (*sourcing*), você poderá executar o nó ouvinte (*listener*):

```bash
source /opt/ros/jazzy/setup.bash
ros2 run demo_nodes_cpp listener
```
Você obterá a seguinte saída:

```bash
[INFO] [1708036800.123456789] [listener]: I heard: "Hello World: 1"
[INFO] [1708036801.123456789] [listener]: I heard: "Hello World: 2"
[INFO] [1708036802.123456789] [listener]: I heard: "Hello World: 3"
```
Pressione `Ctrl + C` para encerrar cada nó em execução e pressione `Ctrl + D` para sair do shell. Após sair do shell, o contêiner ainda pode estar rodando em segundo plano. Você pode parar o contêiner usando o comando da próxima seção.

> **Observação Técnica**:
>
> Quando você abre um novo terminal do Docker com o comando `docker exec`, ele inicia uma nova sessão de shell "limpa". No ROS 2, isso é um desafio comum por causa do isolamento do ambiente.
>
>Aqui está o porquê de precisarmos repetir esse processo:
>
> **O Papel do `setup.bash`**
>
> O ROS 2 não instala seus binários nos caminhos padrão do sistema (como o `/usr/bin`). Em vez disso, ele os mantém organizados em `/opt/ros/jazzy/`. Para que o terminal saiba onde encontrar os comandos `ros2 run`, `ros2 topic`, etc., o script `setup.bash` precisa:
>
> 1. Configurar a variável `$PATH`.
> 2. Definir a variável `$ROS_DISTRO`.
> 3. Configurar caminhos de bibliotecas (`LD_LIBRARY_PATH`) para que o Python e o C++ funcionem.
>
> **Por que no Docker é diferente?**
>
>Em uma instalação nativa no Ubuntu, nós geralmente adicionamos a linha `source /opt/ros/jazzy/setup.bash` ao arquivo `~/.bashrc`. No entanto, em containers Docker:
>
> * **Sessões não-interativas:** Algumas formas de entrar no container não carregam o `.bashrc` automaticamente.
> * **Imagens Oficiais:** Muitas imagens base não vêm com essa linha configurada no `.bashrc` por padrão para permitir que o usuário escolha qual workspace quer carregar.
>
> **Como automatizar isso?**
>
>Para não ter que digitar o comando toda vez, você pode rodar este comando **uma única vez** dentro do seu container:
>
>```bash
>echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
>```
>
>Isso fará com que qualquer novo terminal aberto via `docker exec -it cont-int-2026-1 bash` já reconheça os comandos do ROS automaticamente.

##### **Passo 4: Iniciando, parando e removendo o container**

Aqui está o comando para parar o container que está em execução:
```bash
docker stop cont-int-2026-1
```

Se você quiser verificar o status de todos os containers no seu computador, use:
```bash
docker ps -a
```

Isso mostrará todos os containers existentes e seus respectivos status, indicando se estão parados ou em execução. Após parar o container, se você desejar iniciá-lo novamente, pode usar o comando `docker start` com o nome do container:
```bash
docker start cont-int-2026-1
```

Depois de iniciar o container, você pode anexar um shell usando o comando `docker exec` para acessar o terminal do container:
```bash
docker exec -it cont-int-2026-1 bash
```

Portanto, uma vez que você cria um container, não precisa criá-lo novamente, a menos que haja alterações na imagem Docker. Você pode simplesmente iniciar e parar o container sempre que quiser.

Se desejar remover o container atual, utilize o comando `docker rm`. Certifique-se de parar o container antes de deletá-lo:
```bash
docker stop cont-int-2026-1
docker rm cont-int-2026-1
```

Após deletar o container, você precisará usar o comando `docker run` novamente para criar um novo.

Exploramos os comandos básicos do Docker. [Aqui você encontra](https://docs.docker.com/get-started/docker_cheatsheet.pdf) uma referência para um "guia de consulta rápida" (*cheat sheet*) de comandos Docker que você pode usar para aprender mais comandos. Agora, vamos discutir outro conceito importante no Docker, chamado **Dockerfile**.

#### **Dockerfile para o ROS 2 Jazzy**

Um **Dockerfile** é um arquivo de texto que contém instruções usadas para construir uma imagem Docker personalizada. Ele define como essa imagem deve ser construída. Então, por que precisamos construir uma imagem Docker personalizada? Imagine que você desenvolveu um software para robôs usando o ROS 2; a execução desse software exige que algumas dependências estejam instaladas. A imagem base do ROS 2 Jazzy que usamos anteriormente pode não ter todas essas dependências. Nesse cenário, podemos escrever um Dockerfile colocando o ROS 2 Jazzy como imagem base e adicionando as dependências e o ambiente para criar uma nova imagem personalizada. O Dockerfile nos ajuda a criar imagens customizadas com os pacotes necessários para rodar a aplicação. Ele é semelhante a uma receita, como um conjunto de instruções para produzir uma imagem. Podemos escrever o Dockerfile usando instruções específicas e construir esse arquivo usando o comando `docker build`.

Aqui está a aparência de um Dockerfile básico para o ROS 2 Jazzy:

```dockerfile
# Imagem Base
FROM osrf/ros:jazzy-desktop-full

# Atualiza os pacotes do Ubuntu e instala o pip
RUN apt update && apt upgrade -y
RUN apt install -y python3-pip

# Comando executado ao iniciar o container
CMD ["/bin/bash"]
```

Você pode navegar até a pasta `fundamentos-ros2/scripts/ros2_jazzy_docker/docker_basics` e encontrará este arquivo como [`Dockerfile`](https://raw.githubusercontent.com/fabiobento/cont-int-2026-1/refs/heads/main/fundamentos-ros2/scripts/ros2_jazzy_docker/docker_basics/Dockerfile). O nome **Dockerfile** é o nome padrão de todos os Dockerfiles, mas você pode nomeá-lo como preferir, como `Dockerfile.basic`, `Dockerfile.cont-int-2006-1`, e assim por diante, caso queira manter vários Dockerfiles para diferentes aplicações. Durante a construção(_**build**_) da imagem Docker, você pode especificar o nome deste Dockerfile e ele construirá a imagem correspondente.

Vamos primeiro construir a imagem Docker personalizada e, depois, explorar como o Dockerfile funciona.

Aqui está o comando usado para construir um Dockerfile e criar uma imagem personalizada. Abra um terminal na mesma pasta onde o Dockerfile está localizado e execute este comando:

```bash
docker build -f Dockerfile -t test_ros2:v0.1 .
```

Onde:

* `docker build` é o comando usado para construir uma imagem Docker.
* `-f Dockerfile` especifica o nome do Dockerfile a ser usado.
* `-t test_ros2:v0.1` especifica o nome e a tag da imagem a ser criada.
* `.` especifica o caminho para o Dockerfile.

Este comando lê o **Dockerfile**, que é especificado com o argumento `-f`, e utiliza o `-t` para indicar o nome da imagem e sua tag (etiqueta). A tag é opcional, mas é recomendável colocar uma tag em cada imagem para identificar a versão caso haja alterações no Dockerfile. Você encontrará um ponto (`.`) ao final, que se refere ao diretório atual. O Dockerfile buscará os arquivos para copiar para o container a partir deste diretório.


> **Observação Técnica:**
>
> Se você quiser copiar um script Python da sua máquina para dentro da imagem do robô usando o comando `COPY`, esse script precisa estar dentro da pasta onde você executou o comando (ou em uma subpasta dela). O Docker não consegue "enxergar" arquivos que estejam em pastas superiores ao ponto (`.`) por questões de segurança.

Após uma construção (*build*) bem-sucedida, você poderá encontrar mensagens como esta no terminal:

![](https://github.com/fabiobento/cont-int-2026-1/raw/main/fundamentos-ros2/imagens/docker-build.png)


Após construir a imagem, podemos criar o container usando o comando `docker run`, como fizemos anteriormente:

```bash
docker run -it --name test_ros_dev test_ros2:v0.1
```
Onde:

* `docker run` é o comando usado para criar um container.
* `-it` especifica que o container deve ser executado em modo interativo e com um terminal.
* `--name test_ros_dev` especifica o nome do container.
* `test_ros2:v0.1` especifica a imagem a ser usada.

Após criar o container, você pode usar o comando `docker exec` para acessar mais terminais (*shells*).

Agora você já tem uma ideia de como construir uma imagem do ROS 2 Jazzy escrevendo o seu próprio Dockerfile, então vamos analisar detalhadamente o Dockerfile mencionado anteriormente.

O Dockerfile começa a partir de uma imagem base do ROS 2 Jazzy. A instrução `FROM` no Dockerfile é usada para indicar qual imagem base estamos utilizando. Depois disso, atualizamos e fazemos o upgrade dos pacotes da imagem base. Essa operação utiliza a instrução `RUN` no Dockerfile. Usando a instrução `RUN`, podemos instalar pacotes na imagem base. A própria operação de *update* & *upgrade* transforma a imagem base em uma imagem personalizada, pois a nova imagem passa a ter os pacotes mais recentes; agora, estamos usando a instrução `RUN` para instalar um novo pacote do Ubuntu chamado `python3-pip` dentro da imagem personalizada. Por fim, a instrução `CMD` especifica o comando que deve ser executado quando iniciamos o container.

> **Observação Técnica:**
>
>* **`RUN` vs `CMD`:** O `RUN` acontece durante a **construção** (no seu computador, uma única vez), enquanto o `CMD` acontece toda vez que você **inicia** o container (no robô ou na Raspberry Pi).
>* **Boas Práticas:** Em nosso caso, poderíamos usar o `RUN` para já deixar o `PyTorch` instalado na imagem, poupando tempo.


O comando `CMD` pode ser sobrescrito fornecendo-se o comando ao final do comando `docker run`. Existe um comando semelhante chamado `ENTRYPOINT` no Dockerfile, que desempenha a mesma função, mas o comando não pode ser sobrescrito no `docker run`.

Vamos analisar alguns Dockerfiles mais complexos para o desenvolvimento baseado em ROS 2. Você pode encontrar Dockerfiles básicos que serão bons para iniciar o desenvolvimento com ROS 2. Se você navegar até `fundamentos-ros2/scripts/ros2_jazzy_docker/docker_basics`, encontrará o [`Dockerfile.basic`](https://raw.githubusercontent.com/fabiobento/cont-int-2026-1/refs/heads/main/fundamentos-ros2/scripts/ros2_jazzy_docker/docker_basics/Dockerfile.basic). O usuário padrão na imagem base do ROS 2 Jazzy é o usuário **root**. Este Dockerfile pode criar um novo usuário, o que restringe as permissões e é mais seguro do que o usuário root. O usuário root tem permissão total para fazer qualquer coisa no Docker. É melhor manter um usuário normal durante o desenvolvimento e usar o comando `sudo` para obter acesso root.

```dockerfile
# Imagem Base
FROM osrf/ros:jazzy-desktop-full

# Nome do usuário a ser criado e IDs de usuário/grupo
ARG USERNAME=robot
ARG USER_UID=1000
ARG USER_GID=1000

# Remove o usuário padrão se ele já existir com o mesmo UID (comum no Ubuntu Noble)
RUN if id -u $USER_UID ; then userdel `id -un $USER_UID` ; fi

# Cria o grupo e o usuário, e adiciona suporte ao sudo sem senha
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt update \
    && apt install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Atualiza os pacotes do sistema e instala o gerenciador de pacotes pip
RUN apt update && apt upgrade -y && apt install -y python3-pip

# Define o shell padrão como bash
ENV SHELL=/bin/bash

# Define o usuário padrão para a execução do container
USER $USERNAME

# Comando padrão para iniciar o shell interativo
CMD ["/bin/bash"]
```
Para construir este arquivo e utilizá-lo, você pode usar os mesmos comandos Docker que utilizou para o primeiro exemplo de Dockerfile.

```bash
docker build -f Dockerfile.basic -t test_ros2_basic:v0.1 .
docker run -it --name test_ros_dev_basic test_ros2_basic:v0.1
```

> **Observação Técnica:**
> * **Segurança:** Rodar como root pode permitir que um script mal escrito ou um erro em um nó do ROS apague arquivos cruciais do sistema de arquivos montado.
> * **Compatibilidade:** Muitas ferramentas de GUI (como o **Rviz2**) e alguns drivers de hardware comportam-se de forma diferente ou mais instável quando executados diretamente como root.

Até agora, vimos containers Docker que interagem com comandos de shell. E quanto ao uso de aplicações com interface gráfica (**GUI**) dentro do container Docker? Sim, isso também é possível. Na próxima seção, veremos como executar ferramentas do ROS 2 com a interface gráfica habilitada.


