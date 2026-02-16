# Roteiro 1: Primeiros Passos com ROS 2

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

Para facilitar a instalação, usaremos um script de shell para automatizar este procedimento de instalação e desinstalação. Você pode encontrar o script `ros2_install_jazzy.sh` na pasta `fundamentos-ros2/scripts/` para instalar o ROS 2 Jazzy, e o `ros2_uninstall_jazzy.sh` para desinstalar o mesmo.

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
    > **Observação Técnica Importante:**
    > A instalação nativa no Windows costuma ser evitada na comunidade acadêmica e de pesquisa justamente pela complexidade de gerenciar dependências e a falta de suporte para muitos pacotes que são desenvolvidos especificamente para Linux. O **WSL 2** tem se tornado o padrão *de facto* para quem não pode abrir mão do Windows.

### **Instalando o ROS 2 Jazzy no Docker**
