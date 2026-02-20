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

Esta linha é o shell do container ROS 2 Jazzy com o nome **cont-int-2026-1**. Se você observar o comando acima, verá que usamos o comando `docker run` para criar um container. Devemos adicionar o nome da imagem; também podemos especificar o nome do container usando o argumento `--name`.

O argumento `-it` no Docker ajuda a interagir com o container, permitindo o envio de comandos de texto através do shell **bash**. O comando `bash` ao final informa ao container Docker para executar o interpretador de comandos bash assim que ele iniciar. Portanto, este comando cria um container Docker com um shell bash interativo e o nome de **cont-int-2026-1**. O nome do container é opcional aqui; se você não incluir um nome, ele atribuirá um aleatoriamente. É melhor definir um nome para que possamos iniciar, parar e deletar este container facilmente.

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

#### **Habilitando Interface Gráfica (GUI) em um container ROS 2 Jazzy**

Nesta seção, veremos como habilitar o suporte a interface gráfica no Docker. Após habilitar o suporte a GUI, poderemos trabalhar tanto com as ferramentas gráficas quanto com as de linha de comando do ROS 2 Jazzy. Então, vamos começar.

Vá até a pasta `fundamentos-ros2/scripts/ros2_jazzy_docker/docker_gui`; dentro dela, você encontrará um Dockerfile semelhante ao `Dockerfile.basic`. O nome do Dockerfile é [`Dockerfile.master_ros2`](https://raw.githubusercontent.com/fabiobento/cont-int-2026-1/refs/heads/main/fundamentos-ros2/scripts/ros2_jazzy_docker/docker_gui/Dockerfile.master_ros2). Estes dois arquivos são bem parecidos, mas a diferença está no comando `docker run`. Você pode ver no mesmo diretórios vários scripts shell junto com o `Dockerfile.master_ros2` para construir imagens (`build_image.sh`), criar (`create_container.sh`), iniciar (`start_container.sh`), parar (`stop_container.sh`) e remover (`remove_container.sh`) os containers Docker. Isso tornará o processo mais fácil do que memorizar todos os comandos do Docker. Além disso, todos os scripts aceitam argumentos de linha de comando nos quais podemos especificar o Dockerfile, o nome do container e assim por diante, para construir a imagem Docker e executar o container.

> **Observação Técnica**
Habilitar a GUI é o que permitirá que você abra janelas do `OpenCV` (`cv2.imshow`), o `Rviz2` ou o `rqt` diretamente do container para a tela do seu Ubuntu 24.04.

#### **Construindo a imagem Docker**

Temos um script chamado [`build_image.sh`](https://raw.githubusercontent.com/fabiobento/cont-int-2026-1/refs/heads/main/fundamentos-ros2/scripts/ros2_jazzy_docker/docker_gui/build_image.sh), que aceita diversos argumentos, como o nome da imagem Docker, nome de usuário e assim por diante, e utiliza o comando `docker build` para construir o Dockerfile.

Discutiremos primeiro o uso do script dentro da pasta. Antes de executar o script, crie uma pasta em sua pasta pessoal (`home`) chamada `master_ros2_ws/src` para armazenar seus pacotes ROS 2. Você pode usar o seguinte comando para fazer isso:

```bash
mkdir -p ~/master_ros2_ws/src

```

Após criar esta pasta, você pode iniciar a construção da imagem Docker usando o comando a seguir. Certifique-se de estar executando-o dentro da pasta `fundamentos-ros2/scripts/ros2_jazzy_docker/docker_gui` do repositório:

```bash
./build_image.sh ros2_gui:v0.1 master_ros2_ws robot

```

Neste script, o primeiro argumento é o nome da imagem Docker personalizada com a versão, o segundo é o nome do workspace do ROS 2 (que será discutido na próxima seção) e o terceiro é o nome de usuário que desejamos criar dentro do Docker.

Após construir a imagem, você pode criar um container usando o script [`create_container.sh`](https://raw.githubusercontent.com/fabiobento/cont-int-2026-1/refs/heads/main/fundamentos-ros2/scripts/ros2_jazzy_docker/docker_gui/create_container.sh):

```bash
./create_container.sh ros2_gui:v0.1 master_ros2_ws ros2_dev

```

Ao executar este script, devemos fornecer o nome da imagem que criamos, o nome do workspace do ROS 2 na máquina hospedeira e o nome do container. O script verificará se você possui uma placa de vídeo NVIDIA e seu driver instalados no seu SO Ubuntu. Se instalados, ele utilizará a aceleração gráfica da placa NVIDIA. Estamos apenas usando o comando `docker run` dentro deste script, mas com múltiplos argumentos para aceleração gráfica, montagem de volumes e o workspace do ROS 2 em nosso SO hospedeiro. Criar um container desta forma fornece o ambiente para executar um aplicativo de interface gráfica (GUI) a partir do terminal, e a interface irá aparecer.

Você obterá um shell após criar o container. Você pode executar o seguinte comando para verificar se a interface gráfica está habilitada ou não no container:

```bash
robot@robot-pc:~/master_ros2_ws$ rviz2
```

Isso iniciará o RViz2, que é uma das ferramentas de interface gráfica (GUI) populares do ROS 2. Você verá o RViz2 na tela desta forma:

![](https://github.com/fabiobento/cont-int-2026-1/raw/main/fundamentos-ros2/imagens/docker-rviz2.png)


Terminamos de criar um container Docker com interface gráfica (GUI) habilitada. O restante do script ajuda a iniciar, parar e remover containers. Então, vamos ver como ele é utilizado.

Inicie um novo terminal do container que está em execução. O argumento que você deve fornecer é o nome do container, que é **ros2_dev**:

```bash
./start_container.sh ros2_dev

```

Após iniciar o novo terminal a partir do container, você notará que ele está no caminho do workspace (espaço de trabalho) do ROS 2 que criamos na máquina hospedeira:

```bash
robot@robot-pc:~/master_ros2_ws$

```

Esta pasta **master_ros2_ws** não está dentro do container Docker, mas sim montada a partir da máquina local. Se você se lembra, criamos um workspace do ROS 2 na máquina local, certo? Essa pasta é o que podemos acessar dentro do Docker. Podemos fazer isso montando o volume da pasta do SO hospedeiro durante a criação do container Docker, utilizando o comando `docker run`.

Esta é uma excelente maneira de trabalhar com diferentes distribuições do ROS 2 no mesmo workspace usando a abstração do Docker. O código-fonte permanece no SO hospedeiro, mas podemos montar o workspace do ROS 2 dentro do container e compilar nosso código com diferentes distribuições, como ROS 2 Jazzy, Iron e Humble.

Podemos até usar uma IDE, como o **VS Code**, para realizar desenvolvimento remoto usando um container Docker. Em resumo, o Docker oferece aos desenvolvedores de robótica a oportunidade de criar rapidamente aplicações em ROS 2 e testá-las em qualquer uma das distribuições.

Para parar o container **ros2_dev** em execução, podemos usar o script `stop_container.sh` dentro da pasta `docker_gui`. Execute este script e forneça o nome do container como argumento para parar qualquer container em execução:

```bash
./stop_container.sh ros2_dev

```

Podemos executar o `remove_container.sh` com o nome do container como argumento para removê-lo:

```bash
./remove_container.sh ros2_dev

```

Passamos por alguns tópicos importantes do Docker que utilizaremos no restante do curso. Você também pode consultar os guias [An Updated Guide to Docker and ROS 2](https://roboticseabass.com/2023/07/09/updated-guide-docker-and-ros2/) e [Docker for Robotics with the Robot Operating System (ROS/ROS 2)](https://github.com/2b-t/docker-for-robotics) para obter mais informações sobre a configuração do ROS 2 com Docker.

Até agora, vimos como trabalhar com uma aplicação de container único. A seguir, veremos como trabalhar com aplicações de múltiplos containers, o que significa que os nós do ROS 2 funcionarão em containers separados, e esses dois nós, rodando nesses containers diferentes, irão se comunicar.

#### **Docker Compose com ROS 2 Jazzy**

O [Docker Compose](https://docs.docker.com/reference/cli/docker/compose/) é outro recurso útil no Docker para aplicações de robótica. Trabalhamos com containers Docker individuais usando ferramentas de linha de comando do Docker. E quanto ao trabalho com múltiplos containers? Por exemplo, em uma aplicação de robótica, temos uma aplicação de *front-end* funcionando em um framework JavaScript, uma aplicação de navegação ROS 2 e uma aplicação de *deep learning* para interagir com essa aplicação de navegação. Nesta situação, será melhor manter os três tipos de aplicações em diferentes imagens Docker e iniciar a comunicação entre elas separadamente a partir de diferentes containers. Nesse tipo de cenário, o `docker-compose` é uma opção melhor, pois ajuda a criar e gerenciar múltiplos containers com um único comando. Também podemos configurar as definições de rede do Docker para que todos esses containers possam se comunicar usando o ROS 2 DDS. A parte do `docker-compose` da ferramenta de linha de comando funciona mais como um plugin. Isso já foi instalado em nosso script de configuração do Docker.

Podemos escrever um arquivo de configuração do docker-compose que contenha a configuração desses múltiplos containers, incluindo a imagem Docker, o nome do container e outras configurações mencionadas no comando `docker run`. Uma vez que esses arquivos de configuração estejam escritos, podemos iniciar esses containers com um único comando.

Você pode encontrar um conjunto de configurações do Docker Compose na pasta `fundamentos-ros2/scripts/ros2_jazzy_docker/docker_compose` do [repositório do curso](https://github.com/fabiobento/cont-int-2026-1/tree/main/fundamentos-ros2/scripts/ros2_jazzy_docker/docker_compose) . O nome padrão de cada arquivo de configuração do docker-compose é `docker-compose.yml`. Você pode encontrar um [arquivo básico de docker compose](https://raw.githubusercontent.com/fabiobento/cont-int-2026-1/refs/heads/main/fundamentos-ros2/scripts/ros2_jazzy_docker/docker_compose/docker-compose-basic.yml) nesta pasta, e esta é a sua aparência:

```yaml
services:
  talker:
    image: osrf/ros:jazzy-desktop-full
    command: ros2 run demo_nodes_cpp talker

  listener:
    image: osrf/ros:jazzy-desktop-full
    command: ros2 run demo_nodes_cpp listener
    depends_on:
      - talker
```

Se você verificar este arquivo de configuração, encontrará a versão do Docker Compose no início do arquivo. Depois disso, poderá ver a seção `services`, que define os containers que serão iniciados como parte deste arquivo de compose. Neste exemplo, `talker` e `listener` são os dois containers iniciados na seção de serviços. Se você observar este container, ele utiliza `ros-jazzy-desktop-full` como imagem e executa os nós de publicador (*publisher*) e assinante (*listener*) no ROS 2 para testes. A tag `depends_on` indica que o serviço `listener` depende do `talker`. O `docker-compose` iniciará o serviço `talker` primeiro, antes de iniciar o `listener`.

>  **Observação Técnica:**
> Por que usar o `depends_on` no seu projeto?
> * **Ordem de Inicialização**: Em seus sistemas, você pode garantir que, por exemplo, o nó de driver da câmera (ex: RealSense ou PTZ) suba completamente antes que o seu nó de **Detecção de Anomalias** tente se conectar ao tópico de imagem.
> * **Rede Isolada**: O Docker Compose cria automaticamente uma rede para esses serviços. Mesmo em containers separados, o `listener` conseguirá "ouvir" o `talker` via DDS como se estivessem no mesmo host.

Para iniciar o arquivo [docker-compose](fundamentos-ros2/scripts/ros2_jazzy_docker/docker_compose/docker-compose.yml), você pode usar o seguinte comando. Certifique-se de estar dentro da pasta de código do docker-compose (`fundamentos-ros2/scripts/ros2_jazzy_docker/docker_compose`):

```bash
docker compose up

```

Isso iniciará e executará todos os serviços definidos no arquivo `.yml`. Ao permitir que você defina serviços, redes e volumes em um único arquivo de configuração YAML, ele simplifica o processo de gerenciamento de aplicações Docker de múltiplos containers.

Você verá a saída deste comando da seguinte forma:

![](https://github.com/fabiobento/cont-int-2026-1/raw/main/fundamentos-ros2/imagens/docker-compose.png)

Se você quiser parar o serviço, você pode usar:

```bash
docker compose down
```

Certifique-se de que seu terminal esteja na pasta `fundamentos-ros2/scripts/ros2_jazzy_docker/docker_compose`.

Você também pode encontrar um arquivo docker-compose detalhado na mesma pasta chamado [`docker-compose1.yml`](fundamentos-ros2/scripts/ros2_jazzy_docker/docker_compose/docker-compose1.yml). Este arquivo mostra mais argumentos que podem ser usados no arquivo de configuração. Para rodar o arquivo `docker-compose1.yml` sem precisar renomeá-lo, você usa a flag `-f` (de *file*).

Para subir os serviços:

```bash
docker compose -f docker-compose1.yml up
```

Para derrubar os recursos:

```bash
docker compose -f docker-compose1.yml down
```

#### **Instalando o ROS 2 Jazzy em robôs**

Vimos como configurar o ROS 2 Jazzy em máquinas de desenvolvimento e agora veremos como configurá-lo em robôs.

Em robôs, utilizamos majoritariamente um computador de placa única (SBC) ou uma placa desenvolvida sob medida com um módulo de computação. Se você examinar as SBCs e os módulos de computação populares disponíveis, encontrará tanto as arquiteturas x86_64 quanto ARM64. Você pode instalar o Ubuntu nessas plataformas e trabalhar com o Docker. Duas placas populares usadas em robôs são a Raspberry Pi e as placas da série NVIDIA Jetson.

Você pode encontrar as placas e [módulos Raspberry Pi](https://www.raspberrypi.com/products/) mais recentes em . As placas e módulos da série Jetson mais recentes podem ser encontrados [no site da _NVIDIA developer_](https://developer.nvidia.com/buy-jetson).

Você pode instalar o Ubuntu 24.04 LTS 64-bit na Raspberry Pi mais recente, e este é o SO de "nível 1" (Tier 1) para o ROS 2 Jazzy, o que significa que você pode instalar o ROS 2 a partir dos binários diretamente usando o script que vimos anteriormente para instalação do ROS 2 disponível em `/fundamentos-ros2/scripts/ros2_install_jazzy.sh` e no [repositório do curso no GitHub](https://raw.githubusercontent.com/fabiobento/cont-int-2026-1/refs/heads/main/fundamentos-ros2/scripts/ros2_install_jazzy.sh). O SO ARM de 32 bits é "nível 3" (Tier 3) para o ROS 2 Jazzy; nesse caso, devemos instalar o ROS 2 compilando o código-fonte. O SO padrão que vem com a Raspberry Pi é chamado Raspberry Pi OS, que é um SO baseado em Debian e possui apenas suporte de nível 3. No entanto, você pode configurar o Docker no Raspberry Pi OS usando o script de configuração do Docker e trabalhar no ROS 2 Jazzy em um Ubuntu 24.04 (SO nível 1) a partir do Docker.

Há uma referência para instalar o Ubuntu 24.04 LTS em uma placa Raspberry Pi [nesse site](https://ubuntu.com/download/raspberry-pi).

Você também pode usar o Docker para configurar o ROS 2 Jazzy na Raspberry Pi usando os seguintes comandos, como já vimos anteriormente:

```bash
docker pull ros:jazzy-ros-core 
docker run -it --rm ros:jazzy-ros-core

```

As placas da série Jetson possuem Ubuntu por padrão, o qual é personalizado com drivers da NVIDIA e o [Jetpack SDK](https://developer.nvidia.com/embedded/jetpack). A NVIDIA mantém seus próprios pacotes Debian para o ROS 2. Você pode instalar o ROS 2 Jazzy deles no SO hospedeiro ou usar o Docker para utilizar o ROS 2 Jazzy. A NVIDIA também fornece os [`jetson-containers`](https://github.com/dusty-nv/jetson-containers) para construir imagens Docker com outras bibliotecas. Existem bibliotecas de IA, ROS, visão, entre outras, e você pode escolher qualquer combinação junto com um script fornecido pela NVIDIA.

Isso é extremamente útil para aplicações de robótica.

Aqui está um exemplo de uso do `jetson-containers` com múltiplas bibliotecas de robótica e IA:

```bash
jetson-containers build --name=my_container pytorch transformers ros:jazzy-desktop
```

> **Observação Técnica:**
> Trabalhar com Docker no computador do robô será a melhor abordagem, pois ajuda na implantação facilitada do software do robô sem se preocupar com dependências. Também ajuda a atualizar o software do robô facilmente, bastando baixar (*pull*) uma nova imagem.

Vimos diferentes métodos de instalação do ROS 2 Jazzy em máquinas de desenvolvimento e computadores de robôs. A próxima aula é sobre o aprendizado de diferentes conceitos e ferramentas no ROS 2.

## Conceitos e Ferramentas Básicas do ROS 2

Nesta seção, exploraremos conceitos importantes do ROS 2 utilizando uma abordagem prática. Precisamos compreender todos esses conceitos antes de começarmos a programar usando o ROS 2 Jazzy. Veremos diferentes ferramentas do ROS 2 juntamente com o entendimento de seus conceitos, explicando cada um deles por meio de um exemplo.

Antes de saltarmos para os conceitos, devemos entender por que usamos o ROS 2 para a programação de robôs. O ROS 2 é um framework de software que fornece um conjunto de bibliotecas, ferramentas e recursos para a construção de suas aplicações robóticas. Então, qual é a característica fundamental que o ROS 2 traz para a programação de robôs? É a **comunicação entre processos** (IPC), ou seja, a comunicação entre os diferentes processos no sistema operacional. Como você sabe, um robô pode ter múltiplos sensores, atuadores e computadores. Os dados dos sensores do robô precisam ser adquiridos e depois processados para gerar sinais de controle para os atuadores. Geralmente, essas operações podem não estar incluídas em um único processo rodando no computador. O principal motivo é que, se qualquer operação falhar, ela pode derrubar o processo inteiro. Escrevemos múltiplos processos para realizar essa operação. É aí que o ROS 2 traz o poder da comunicação entre processos; ele pode fornecer diferentes APIs em C++/Python e ajudar esses programas a trocar dados de diferentes maneiras. Os dados podem ser enviados continuamente para outro programa, como uma interação de requisição e resposta. Esta é uma funcionalidade central que o ROS 2 oferece aos desenvolvedores de robótica. Todas as outras funcionalidades são construídas sobre este recurso principal. 

Primeiro, veremos como executar um programa no ROS 2. Não escreveremos um programa novo para executá-lo; em vez disso, tentaremos rodar um programa já existente, que está disponível no ROS 2 assim que você o instala.

### Como executar nós/aplicativos do ROS 2 no seu robô

Como já sabemos, usando o ROS 2, podemos criar nossos próprios nós/aplicativos de robótica para realizar tarefas específicas no robô. Veremos exatamente como executar esses nós a seguir:

1. O ROS 2 fornece uma ferramenta de linha de comando chamada `ros2`. Esta ferramenta nos ajuda a realizar múltiplas operações no framework ROS 2. Vamos começar com sua máquina que possui o ROS 2 instalado; pode ser o seu SO hospedeiro ou um container Docker.

    Primeiro, abra um terminal e, para demonstração, utilizaremos o container Docker que foi criado anteriormente com suporte a interface gráfica (GUI).

    Execute este script a partir da pasta `fundamentos-ros2/scripts/ros2_jazzy_docker/docker_gui`:

    ```bash
    ./start_container.sh ros2_dev
    ```

2. Execute o comando `ros2` no seu terminal:

    ```bash
    $ ros2
    ```

Se o seu ambiente ROS 2 estiver configurado corretamente, você verá esta saída no terminal:


![](https://github.com/fabiobento/cont-int-2026-1/raw/main/fundamentos-ros2/imagens/ros2-app.png)


O comando `ros2` é o comando principal no ROS 2, o qual vem acompanhado de subcomandos, conforme mostrado na Figura 2.7. Você encontrará subcomandos como `run`, que auxilia na execução de um nó específico do ROS 2. A partir da lista acima, é possível identificar o uso de cada subcomando. Você pode consultar a utilidade de cada um simplesmente inserindo-o no terminal. Por exemplo, se digitar `ros2 run`, verá os sub-argumentos que devem ser passados por este terminal. O comando `ros2` é o comando principal da CLI (Interface de Linha de Comando) do ROS 2.

3. Para executar um programa/executável específico do ROS 2, use o seguinte comando:

```bash
ros2 run nome_do_pacote_ros nome_do_executavel
```

Ex:

```bash
ros2 run demo_nodes_cpp talker
```

Neste exemplo, `demo_nodes_cpp` é um pacote ROS 2 e `talker` é o nome do executável do programa em C++ dentro deste pacote. O `demo_nodes_cpp` é instalado juntamente com o ROS 2 Jazzy.

Você deve estar se perguntando o que é um pacote ROS 2. Então, vamos ver o que é um pacote ROS 2 e prosseguir com o comando `ros2 run`.

### O que é um pacote ROS 2?

Um pacote ROS 2 é uma organização de software dentro do framework ROS 2. Ele contém o código e os arquivos necessários para implementar funcionalidades ou recursos específicos em uma aplicação robótica. Tipicamente, um pacote ROS 2 compreende nós (programas que executam computações), bibliotecas, arquivos de configuração, arquivos de inicialização (*launch files*) e outros recursos, como definições de mensagens e serviços.

Tudo no ROS 2 é modelado dentro de um pacote. Um pacote é simplesmente uma pasta que podemos criar usando o comando `ros2 pkg`, e que conterá arquivos como `package.xml`, `CMakeLists.txt`, e assim por diante, para manter a identidade do pacote. Informações como o nome do pacote, dependências e outras serão incluídas nesses arquivos.
Ao instalarmos o ROS 2, obteremos seus pacotes principais por padrão. Também teremos acesso a toneladas de pacotes ROS 2 da comunidade. Esses pacotes são facilmente redistribuídos via Git ou podem ser adicionados aos repositórios oficiais do ROS 2, permitindo a instalação de seus binários.

Um recurso útil do ROS 2 é a facilidade de reutilizar pacotes construídos por outros desenvolvedores em seu robô. Cada pacote é criado para aplicações específicas. Por exemplo, o pacote `demo_nodes_cpp` no ROS 2 contém exemplos de C++ para o ROS 2.

Veremos mais detalhes sobre a estrutura de um pacote ROS 2 nas próximas seções.

Retornando ao comando `ros2 run`, você pode notar que o primeiro argumento mencionado é o nome do pacote e, em seguida, o nome do executável. Se você estiver escrevendo um programa em C++ usando ROS 2, ele deve ser compilado e obteremos um executável. Neste exemplo, esse executável é o que mencionamos no comando. Estes exemplos de demonstração já foram instalados com o ROS 2. Se você criar um pacote ROS 2 com programas em C++, podemos compilar esses programas e gerar o executável. No próximo capítulo, aprenderemos como criar um pacote e inserir código C++ dentro dele.

Ao executar este comando de exemplo, você verá o executável começar a rodar:

```bash
[INFO] [1726326377.958376860] [talker]: Publishing: 'Hello World: 1'
[INFO] [1726326378.958355664] [talker]: Publishing: 'Hello World: 2'
[INFO] [1726326379.958358086] [talker]: Publishing: 'Hello World: 3'
```

Assim que o executável começa a rodar, um nó ROS 2 será criado.

### O que é um nó (node) ROS?

Quando você inicia um executável ROS 2, ele rodará e se tornará um processo. Este processo é chamado de nó ROS 2. Portanto, quando escrevemos um programa em C++/Python usando APIs do ROS 2 e compilamos/construímos e executamos o executável, obtemos um nó ROS 2. Um nó ROS 2 é um processo único que realiza algum tipo de computação, como coletar dados de sensores, processar esses dados ou outras operações no PC do robô ou do operador. Nós no ROS 2 podem publicar e assinar diversos tipos de dados com a ajuda do middleware DDS subjacente. Uma aplicação robótica terá um conjunto de nós ROS 2 para diferentes propósitos. Cada nó pode ser iniciado usando o `ros2 run`; outras técnicas, como o arquivo `ros2 launch`, permitem iniciar múltiplos nós com um único comando.

Para inspecionar os detalhes completos de um nó ROS 2, podemos usar o comando `ros2 node`. Este comando nos fornece informações sobre o nó específico que mencionamos e uma lista de nós em execução no SO.

Se você executar o comando `ros2 node list` em um novo terminal, ele listará os nós em execução. Neste exemplo, a saída do comando é `/talker`.

`/talker` não é o nome do nosso executável; em vez disso, o nome do nó é o que atribuímos dentro do próprio código. Isso não está visível para nós agora. No próximo capítulo, demonstraremos o mesmo. Você pode dar qualquer nome ao seu nó, e dois nós não podem ter o mesmo nome. Seus nomes devem ser únicos!

O comando a seguir listará os detalhes desses nós, o que inclui Assinantes (*Subscribers*), Publicadores (*Publishers*), Serviços e Ações:

```bash
ros2 node info /talker
```

Aqui está como veremos a saída do mesmo:

```bash
Subscribers:
Publishers:
/chatter: std_msgs/msg/String
Service Servers:
Service Clients:
Action Servers:
Action Clients:
```

Nesta saída, não há Assinantes, Servidores de Serviço, Clientes ou Servidores de Ação, mas você pode encontrar um nome de Publicador, `/chatter`. Ainda não sabemos muito sobre Publicadores, Assinantes, Serviços e Ações do ROS 2. Esses termos referem-se a padrões de comunicação entre os diferentes nós. Será melhor compreender esses termos antes de retornar a este ponto.

### O que é um tópico ROS?

Vimos os termos Publicador (*Publisher*) e Assinante (*Subscriber*) na saída do comando anterior. Um publicador em um nó pode enviar um tipo de dado, e o assinante também pode receber um tipo de dado. Os nós publicam e assinam diversos tipos de dados por meio dos tópicos ROS. Os tópicos ROS são um meio de comunicação entre diferentes nós. Ele é chamado de barramento de dados nomeado, no qual os nós podem trocar vários tipos de dados. Podemos criar qualquer número de tópicos em nosso nó ROS e enviar diversos tipos de dados, como inteiros, floats, matrizes, imagens e assim por diante. Também podemos assinar vários tipos de dados dentro de um nó ROS. Os tópicos ROS são um tipo de comunicação que usamos nos nós ROS. A comunicação com tópicos ROS é assíncrona, o que significa que o publicador pode enviar dados contínuos sem esperar pelo nó receptor. O publicador nem sequer sabe muito sobre quem está recebendo os dados. Podemos dizer que é um mecanismo de comunicação de N-para-M.

No exemplo acima, o tópico para publicação de dados é `/chatter` (`std_msgs/msg/String`). Junto com o nome do tópico, você pode ver o tipo de dado que ele está publicando: uma string (*cadeia de caracteres*). Na próxima seção, aprenderemos mais sobre os diferentes tipos de dados do ROS.

Podemos agora iniciar um nó assinante chamado `listener`, que está inscrito no mesmo tópico `/chatter`. Aqui está o comando para rodar o nó `listener`:

```bash
ros2 run demo_nodes_cpp listener

```

Certifique-se de ter aberto um novo terminal para executar este comando. Além disso, não confunda o nome do executável com o nome do nó aqui. O nome do nó é definido dentro do código e o executável é apenas um arquivo binário. Neste exemplo, o nome do nó e o executável são iguais, mas não serão os mesmos em todos os casos.

Você obterá a seguinte saída com o nó `listener`:

```bash
[INFO] [1726333039.114079927] [listener]: I heard: [Hello World: 1]
[INFO] [1726333040.113948341] [listener]: I heard: [Hello World: 2]
[INFO] [1726333041.113945517] [listener]: I heard: [Hello World: 3]
```

Após rodar os nós `talker` e `listener`, você pode executar o seguinte comando:

```bash
ros2 node list
```

E a saída será:

```bash
/listener
/talker
```

Esta saída mostra que, atualmente, dois nós estão rodando em nosso sistema. Se tentarmos o comando `ros2 node info /listener`, ele mostrará o tópico ao qual o nó `/listener` está inscrito:

```bash
Subscribers:
/chatter: std_msgs/msg/String
Publishers:
```

Se quisermos ver como os nós estão se comunicando, podemos usar uma ferramenta de interface gráfica (GUI) do ROS 2 chamada `rqt`. Abra um novo terminal e digite `rqt`, e você verá uma janela vazia. Vá em **Plugins | Introspection | Node Graph**. Você verá uma saída como esta:

![](https://github.com/fabiobento/cont-int-2026-1/raw/main/fundamentos-ros2/imagens/ros2-rqt.png)