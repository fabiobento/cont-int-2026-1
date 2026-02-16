# Roteiro: Primeiros Passos com Programação em ROS 2

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

Para acompanhar este roteiro, é recomendável ter um computador ou placa embarcada (por exemplo, Raspberry Pi, placa Jetson, etc.) com o Ubuntu 24.04 LTS instalado ou qualquer outra versão do Ubuntu. Se você não possui o Ubuntu em sua máquina.

Os materiais de referência para este roteiro podem ser encontrados na pasta Chapter02 do seguinte repositório no GitHub: https://github.com/fabiobento/Mastering-ROS-2-for-Robotics-Programming/tree/main/Chapter02.

## Instalação do ROS 2

Os computadores da maioria dos robôs rodam uma distribuição **Linux**, sendo o **Ubuntu** a mais comum. O computador a ser escolhido para o robô depende dos requisitos da aplicação robótica; podem ser PCs industriais com arquitetura x86_64 ou módulos de computação baseados em ARM64, como o Jetson Orin ou o Raspberry Pi.

Como você sabe, faremos o **deploy (implantação)** da aplicação no **computador do robô**.
- No entanto, o desenvolvimento do software de robótica ocorrerá, na maioria das vezes, em uma estação de trabalho ou laptop de desenvolvedor, que pode estar equipado com Windows, Ubuntu ou macOS.
- Então o ROS 2 pode ser instalado em todas as plataformas?
    - Sim. Isso é possível com a ajuda de ferramentas como Docker, VirtualBox, VMware, UTM e assim por diante.
- Vamos explorar diferentes maneiras de instalar o ROS 2 em um robô e em nossa máquina de desenvolvimento.