# **Aula 3: Tópicos – Enviando e Recebendo Mensagens entre Nós**

Agora que já sabe escrever nós, como pode fazer com que vários nós se comuniquem entre si, e como pode interagir com nós existentes em uma aplicação?

Existem três tipos de comunicação no ROS 2:
- Tópicos
- Serviços
- Ações

Nesta aula, vamos estudar tópicos do ROS 2.

Para entender como os tópicos funcionam, começaremos com uma analogia da vida real. Isso permitirá que você compreenda o conceito usando conhecimentos prévios e comuns. Em seguida, você estudará o código e escreverá um publicador (*publisher*) e um assinante (*subscriber*) dentro de um nó — primeiro com interfaces existentes e, depois, construindo interfaces personalizadas. Você também usará ferramentas do ROS 2, como a linha de comando `ros2` e o `rqt_graph`, para inspecionar os tópicos e desbloquear mais funcionalidades.

Ao final dessa aula, você será capaz de fazer seus nós se comunicarem entre si usando tópicos do ROS 2. Você aprenderá escrevendo código e receberá um desafio adicional no final dessa aula.

Os tópicos são usados em toda parte no ROS 2. Quer você deseje criar uma aplicação do zero ou usar plugins existentes do ROS, você terá que usar tópicos.

## **O que é um tópico ROS 2?**

Você já teve contato com o conceito de tópicos através do controle da tartaruga pelo teclado na Aula 1. Nesse experimento, o nó do teclado enviava comandos de velocidade para o nó da tartaruga. Com isso, você já deve ter uma intuição básica de como as coisas funcionam.

Agora vamos explicar os tópicos usando uma analogia da vida real que facilita o entendimento. Vamos construir um exemplo, passo a passo, e depois recapitular os pontos mais importantes.

### *Um publicador (*publisher*) e um assinante (*subscriber*)**

Para esta analogia, usaremos transmissores e receptores de rádio. Como este é um exemplo simplificado, nem tudo o que direi sobre rádio será tecnicamente correto, mas o objetivo aqui é entender os tópicos do ROS 2.

Vamos começar com um transmissor de rádio. Este transmissor enviará alguns dados em uma determinada frequência. Para facilitar a memorização, essa frequência geralmente é representada por um número, como 98,7. Podemos até pensar em 98,7 como um nome. Se você quiser ouvir rádio, sabe que precisa conectar seu dispositivo à 98,7.

Neste caso, podemos dizer que **98,7 é um tópico**. O transmissor de rádio é um **publicador** neste tópico:



![](https://github.com/fabiobento/cont-int-2026-1/raw/main/topics-ros2/imagens/radio-pub.jpg)
**Transmissor de rádio publicando no tópico 98,7.** ([Fonte](https://www.packtpub.com/en-us/product/ros-2-from-scratch-9781835881415))

Agora, digamos que você queira ouvir essa rádio do seu celular. Você pedirá ao seu celular para se conectar à 98.7 para receber os dados.

Com essa analogia, o celular é então um **assinante** do tópico 98.7.

Uma coisa importante a notar aqui é que tanto o transmissor de rádio quanto o celular devem usar o mesmo tipo de frequência. Por exemplo, se o transmissor de rádio estiver usando um sinal AM, e o celular tentar decodificar um sinal FM, isso não vai funcionar.

Da mesma forma, com os tópicos do ROS 2, tanto o publicador quanto o assinante devem usar o mesmo tipo de dado. Esse tipo de dado é chamado de **interface** (ou mensagem).

É isso que define um tópico: um **nome** e uma **interface**:

![](https://github.com/fabiobento/cont-int-2026-1/raw/main/topics-ros2/imagens/radio-pub-sub.jpg)
**Publicador e assinante usando a mesma interface** ([Fonte](https://www.packtpub.com/en-us/product/ros-2-from-scratch-9781835881415))


Com isso, a comunicação está completa. O transmissor de rádio publica um sinal AM no tópico 98.7. O celular assina o tópico 98.7, decodificando um sinal AM.

### **Múltiplos publicadores e assinantes**

Na vida real, não haverá apenas um dispositivo tentando ouvir a rádio. Vamos adicionar mais alguns dispositivos, cada um assinando o tópico 98.7 e decodificando um sinal AM:

![](https://github.com/fabiobento/cont-int-2026-1/raw/main/topics-ros2/imagens/radio-pub-sub-mult.jpg)
**Tópico com vários assinantes** ([Fonte](https://www.packtpub.com/en-us/product/ros-2-from-scratch-9781835881415))

Como você pode ver, um tópico pode ter vários assinantes. Cada assinante receberá os mesmos dados. Por outro lado, também poderíamos ter vários publicadores para um único tópico.

Imagine que há outro transmissor de rádio, também publicando um sinal AM na 98.7. Neste caso, os dados tanto do primeiro quanto do segundo transmissor são recebidos por todos os dispositivos ouvintes:

![](https://github.com/fabiobento/cont-int-2026-1/raw/main/topics-ros2/imagens/radio-pub-mult-sub-mult.jpg)
**Tópico com vários publicadores e vários assinantes** ([Fonte](https://www.packtpub.com/en-us/product/ros-2-from-scratch-9781835881415))

A figura anterior mostra caixas. Cada caixa representa um nó. Assim, temos dois nós transmissores de rádio, ambos contendo um publicador para o tópico 98.7. Também temos três nós (celular, receptor de rádio e carro), cada um contendo um assinante da 98.7.

Note que um assinante não tem conhecimento dos outros assinantes. Quando você ouve a rádio no seu celular, não faz ideia de quem mais está ouvindo a rádio e em qual dispositivo.

Além disso, o celular, o receptor de rádio e o carro não sabem quem está publicando na rádio. Eles apenas sabem que têm que assinar a 98.7; eles não sabem o que está por trás disso.

Por outro lado, ambos os transmissores de rádio não têm conhecimento um do outro nem de quem está recebendo os dados. Eles apenas publicam no tópico, independentemente de quem está ouvindo. Portanto, dizemos que os tópicos são **anônimos**. Publicadores e assinantes não têm conhecimento de outros publicadores e assinantes. Eles apenas publicam ou assinam um tópico, usando seu nome e interface.

Qualquer combinação de publicadores e assinantes é possível. Por exemplo, você pode ter dois publicadores no tópico e zero assinantes. Neste caso, os dados ainda são publicados corretamente, mas ninguém os recebe. Alternativamente, você poderia ter zero publicadores e um ou mais assinantes. Os assinantes ouvirão o tópico, mas não receberão nada.


###  **Múltiplos publicadores e assinantes dentro de um nó**

Um nó não está limitado a ter apenas um publicador ou um assinante.

Vamos adicionar outra rádio ao nosso exemplo. Vamos chamá-la de 101.3, e seu tipo de dado é sinal FM.

O segundo transmissor de rádio agora está publicando tanto no tópico 98.7 quanto no tópico 101.3, enviando o tipo de dado apropriado para cada tópico. Vamos também fazer o carro ouvir o tópico 101.3:


![](https://github.com/fabiobento/cont-int-2026-1/raw/main/topics-ros2/imagens/radio-2pub-node.jpg)
**Um nó com dois publicadores** ([Fonte](https://www.packtpub.com/en-us/product/ros-2-from-scratch-9781835881415))


Como você pode ver, o segundo transmissor de rádio pode publicar em vários tópicos, desde que use o nome e a interface corretos para cada tópico.

Agora, imagine que o carro, enquanto ouve a rádio, também está enviando suas coordenadas GPS para um servidor remoto. Poderíamos criar um tópico chamado `car_location`, e a interface conteria uma latitude e uma longitude. O nó do carro agora contém um assinante do tópico 98.7 e um publicador para o tópico `car_location`:

![](https://github.com/fabiobento/cont-int-2026-1/raw/main/topics-ros2/imagens/radio-pub-sub-node.jpg)
**Um nó com tanto um publicador quanto um assinante** ([Fonte](https://www.packtpub.com/en-us/product/ros-2-from-scratch-9781835881415))


Na figura anterior, também adicionei outro nó para o servidor, representado por um computador. O nó do servidor assinará o tópico `car_location` para que possa receber as coordenadas GPS. Obviamente, tanto o publicador quanto o assinante estão usando a mesma interface (latitude e longitude).

Assim, dentro de um nó, você pode ter qualquer número de publicadores e assinantes para diferentes tópicos com diferentes tipos de dados. Um nó pode se comunicar com vários nós ao mesmo tempo.
### **Resumindo**

Os nós do ROS 2 podem enviar mensagens para outros nós usando tópicos.

Os tópicos são usados principalmente para enviar fluxos de dados (*data streams*). Por exemplo, você poderia criar um *driver* de hardware para um sensor de câmera e publicar as imagens capturadas por ela. Outros nós podem então assinar o tópico e receber as imagens. Você também poderia publicar um fluxo de comandos contínuos para fazer um robô se mover, e assim por diante.

Há muitas possibilidades para o uso de tópicos, e você conhecerá mais sobre elas à medida que progredirmos.

> Aqui estão alguns pontos importantes sobre como os tópicos funcionam:
>
> * Um tópico é definido por um **nome** e uma **interface**.
> * O nome de um tópico deve começar com uma letra e pode ser seguido por outras letras, números, sublinhados (*underscores*), tis (*tildes*) e barras (*slashes*). Para a analogia da vida real com a rádio, usei números com pontos como nomes de tópicos. Embora isso tenha facilitado os exemplos, não é válido para tópicos do ROS 2. Para torná-lo válido, em vez de `98.7`, teríamos que criar um tópico chamado `radio_98_7`.
> * Qualquer publicador ou assinante de um tópico deve usar a **mesma interface**.
> * Publicadores e assinantes são **anônimos**. Eles não têm conhecimento uns dos outros; apenas sabem que estão publicando ou assinando um tópico.
> * Um nó pode conter vários publicadores e assinantes para **tópicos diferentes**.

## Requisitos Técnicos 

### **Passo 1: Isolamento de Rede no Laboratório (Obrigatório)**

Como estamos todos conectados à mesma rede Wi-Fi, o ROS 2 tentará conectar os nós de todos os computadores automaticamente. Se não isolarmos a rede, o seu controlador tentará mover o robô do colega ao lado!

Para evitar isso, cada aluno receberá um número de identificação (ID) único  correspondente a sua bancada.

Abra o terminal e verifique se a variável de ambiente `ROS_DOMAIN_ID` está vazia:
```bash
echo $ROS_DOMAIN_ID
```

Caso esteja vazia ou não esteja com o número de sua bancada, abra o Terminal e exporte a variável ambiental `ROS_DOMAIN_ID` **antes** de rodar qualquer comando ROS 2 da seguinte forma:

1. Adicione o comando ao final do arquivo `.bashrc` (substitua XX pelo número de sua bancada, ex: export ROS_DOMAIN_ID=7)
    ```bash
    echo "export ROS_DOMAIN_ID=XX" >> ~/.bashrc
    ```

2. Recarregue as configurações para aplicar no terminal atual
    ```bash
    source ~/.bashrc
    ```

###  **Passo 2: Preparando o Ambiente: Obtendo o Código da Disciplina**

Para realizarmos as práticas de ROS 2, você precisará dos scripts, *packages* e arquivos de configuração mais recentes. Todo o material é atualizado constantemente no repositório da disciplina no GitHub.

Siga as instruções abaixo de acordo com a sua situação no laboratório de hoje:

**1. Primeira vez usando o repositório (Ainda não baixou)**
Se você está usando um computador novo no laboratório ou ainda não baixou o material deste semestre, abra o Terminal e execute o comando de clonagem para trazer o projeto para a sua máquina:

```bash
cd
git clone https://github.com/fabiobento/cont-int-2026-1.git
```

**2. Atualizando o repositório existente (Já baixou anteriormente)**
Se você já tem a pasta do projeto no seu computador, precisaremos sincronizá-la com as atualizações da semana.

> **Atenção:** Durante as aulas práticas, é esperado e recomendável que vocês editem os códigos para testar hipóteses. No entanto, para iniciar a aula de hoje sem erros de conflito, usaremos uma sequência de comandos que baixa as novidades e **sobrescreve** qualquer alteração local. Isso garante que o seu ambiente fique exatamente igual à versão oficial para o roteiro de hoje.

Abra o Terminal e execute a seguinte sequência:

```bash
cd ~/cont-int-2026-1
git fetch
git reset --hard origin/main
```

**O que esses comandos fazem?**

* **`cd cont-int-2026-1`**: Garante que você está dentro da pasta correta do projeto.
* **`git fetch`**: Consulta o GitHub e baixa silenciosamente as informações mais recentes do servidor, mas ainda não altera os seus arquivos visíveis.
* **`git reset --hard origin/master`**: Força os seus arquivos locais a ficarem idênticos à ramificação principal (`master`) oficial, descartando testes e modificações residuais das aulas anteriores.


## **Escrevendo um publicador de tópico**

Nesta seção, você escreverá seu primeiro publicador (*publisher*) no ROS 2. Para trabalhar nos conceitos centrais, criaremos uma nova aplicação ROS 2 e a expandiremos nas próximas aulas. Esta aplicação será super minimalista para que possamos focar apenas no conceito que queremos aprender, e em nada mais.

O que queremos fazer por enquanto é publicar um número em um tópico. Este tópico é novo e nós o criaremos. Na verdade, você não "cria" um tópico diretamente — você cria um publicador ou um assinante para esse tópico. Isso criará automaticamente o nome do tópico, que será registrado no grafo computacional.

Para escrever um publicador, precisamos de um nó. Poderíamos usar o primeiro nó que criamos nas aulas anteriores, mas o propósito do nó não é o mesmo. Portanto, criaremos um novo nó chamado `number_publisher`. Neste nó, criaremos um publicador. Quanto ao tópico no qual queremos publicar, teremos que escolher um nome e uma interface.

Agora, vamos começar com o Python.

### **Escrevendo um publicador em Python**

Para escrever um publicador, precisamos criar um nó; para criar um nó, precisamos de um pacote. Para simplificar as coisas, vamos continuar usando o pacote `my_py_pkg`.

**Criando um nó**

Navegue até o interior do pacote `my_py_pkg`, crie um arquivo Python e torne-o executável:

```bash
cd ~/master_ros2_ws/src/my_py_pkg/my_py_pkg/
touch number_publisher.py
chmod +x number_publisher.py
```

Agora, abra este arquivo python que acabou de criar, e utilize o template de nó orientado a objetos (disponibilizado na Aula 2 - [Template para um nó Python](https://github.com/fabiobento/cont-int-2026-1/blob/main/nodes-ros2/scripts/node_oop_template/node_oop_template.py)) e modifique os campos necessários para usar nomes que façam sentido:

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node


class NumberPublisherNode(Node):
    def __init__(self):
        super().__init__("number_publisher")


def main(args=None):
    rclpy.init(args=args)
    node = NumberPublisherNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
```

Agora que você tem uma função `main()` e uma classe `NumberPublisherNode` para o seu nó, podemos criar um publicador.

**Adicionando um publicador ao nó**

Onde podemos criar um publicador neste nó? Faremos isso no construtor.

> E antes de escrevermos o código, precisamos nos fazer uma pergunta: qual é o nome e a interface para este tópico?
> 
> * **Caso 1:** Você está publicando em um tópico que já existe (outros publicadores ou assinantes nesse tópico), e então você usa o mesmo nome e interface.
> * **Caso 2:** Você cria um publicador para um tópico novo (o que estamos fazendo agora), e então você precisa escolher um nome e uma interface.

Para o nome, vamos manter as coisas simples e usar `number`. Se publicarmos um número, podemos esperar receber esse número em um tópico `number`. Se você fosse publicar uma temperatura, poderia nomear o tópico como `temperature`.

Para a interface, você tem duas escolhas: usar uma interface existente ou criar uma personalizada. Para começar, usaremos uma interface existente. Para facilitar, eu simplesmente direi qual usar; você aprenderá a encontrar outras interfaces por conta própria mais tarde.

Vamos usar `example_interfaces/msg/Int64`. Para obter mais detalhes sobre o que há na interface, podemos rodar `ros2 interface show <nome_da_interface>` no Terminal:

```bash
ros2 interface show example_interfaces/msg/Int64
# Alguns comentários
int64 data
```

Isso é exatamente o que precisamos: um número `int64`.

Agora que temos essa informação, vamos criar o publicador. Primeiro, importe a interface e, em seguida, crie o publicador no construtor:

```python
import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64

class NumberPublisherNode(Node):
    def __init__(self):
        super().__init__("number_publisher")
        self.number_publisher_ = self.create_publisher(Int64,"number", 10)
```  

Para importar a interface, devemos especificar o nome do pacote (`example_interfaces`), depois o nome da pasta para mensagens de tópico (`msg`) e, finalmente, a classe para a interface (`Int64`).

Para criar o publicador, devemos usar o método `create_publisher()` da classe `Node`. Herdar dessa classe nos dá acesso a todas as funcionalidades do ROS 2. Neste método, você deve fornecer três argumentos:

* **Interface do tópico:** Usaremos `Int64` do pacote `example_interfaces`.
* **Nome do tópico:** Como definido anteriormente, este é `number`.
* **Tamanho da fila (*Queue size*):** Se as mensagens forem publicadas muito rápido e os assinantes não conseguirem acompanhar, as mensagens serão armazenadas em um *buffer* (até 10, neste caso) para que não sejam perdidas. Isso pode ser importante se você enviar mensagens grandes (como imagens) em alta frequência, em uma rede com perda de pacotes. Como estamos apenas começando, não há necessidade de se preocupar com isso; recomendo que você simplesmente defina o tamanho da fila como `10` todas as vezes.

Com isso, agora temos um publicador no tópico `number`. No entanto, se você simplesmente executar seu código assim, nada acontecerá. Um publicador não publicará automaticamente em um tópico. Você tem que escrever o código para que isso aconteça.

**Publicando com um temporizador (*Timer*)**

Um comportamento comum em robótica é realizar uma ação *X* a cada *Y* segundos — por exemplo, publicar uma imagem de uma câmera a cada 0,5 segundos ou, neste caso, publicar um número em um tópico a cada 1,0 segundo. Como visto na **Aula 2**, para fazer isso, você deve implementar um temporizador e uma função de *callback*.

Modifique o código dentro do nó para que você publique no tópico a partir de um *callback* de temporizador:

```python
def __init__(self):
    super().__init__("number_publisher")
    self.number_ = 2
    self.number_publisher_ = self.create_publisher(Int64, "number",10)
    self.number_timer_ = self.create_timer(1.0, self.publish_number_callback)
    self.get_logger().info("O publicador de números foi iniciado.")

def publish_number_callback(self):
    msg = Int64()
    msg.data = self.number_
    self.number_publisher_.publish(msg)
```

Após criar o publicador com `self.create_publisher()`, criamos um temporizador (*timer*) com `self.create_timer()`. Aqui, dizemos que queremos que o método `publish_number()` seja chamado a cada `1.0` segundo. Isso acontecerá enquanto o nó estiver em execução (processando o `spin`).

Além disso, também adicionei um *log* no final do construtor para informar que o nó foi iniciado. Geralmente faço isso como uma boa prática, para poder ver no Terminal quando o nó está totalmente inicializado.

No método `publish_number()`, nós publicamos no tópico:

* Criamos um objeto a partir da classe `Int64`. Esta é a interface — em outras palavras, a mensagem a ser enviada.
* Este objeto contém um campo `data`. Como sabemos disso? Descobrimos isso anteriormente quando rodamos `ros2 interface show example_interfaces/msg/Int64`. Portanto, fornecemos um número no campo `data` da mensagem. Por simplicidade, especificamos o mesmo número toda vez que executamos a função de *callback*.
* Publicamos a mensagem usando o método `publish()` do publicador.

Esta estrutura de código é super comum no ROS 2. Sempre que você quiser publicar dados de um sensor, você escreverá algo semelhante.

Aqui está o código completo para o nó publicador em Python *(também disponível [**nesse link**](https://github.com/fabiobento/cont-int-2026-1/blob/main/topics-ros2/scripts/my_py_pkg/my_py_pkg/number_publisher.py))*:

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64

class NumberPublisherNode(Node):
    def __init__(self):
        super().__init__("number_publisher")
        self.number = 2
        self.number_publisher_ = self.create_publisher(Int64,"number", 10)        
        self.number_timer_ = self.create_timer(1.0, self.publish_number_callback)
        self.get_logger().info("O publicador de números foi iniciado.")      

    def publish_number_callback(self):
        msg = Int64()
        msg.data = self.number
        self.number_publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = NumberPublisherNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
```

**Compilando o publicador**

Para testar seu código, você precisa instalar o nó.

Antes de fazermos isso, como estamos usando uma nova dependência (o pacote `example_interfaces`), também precisamos adicionar uma linha ao arquivo `package.xml` do pacote `my_py_pkg`:

```xml
<depend>rclpy</depend>
<depend>example_interfaces</depend>
```

À medida que você adicionar mais funcionalidades dentro do seu pacote, você adicionará qualquer outra dependência do ROS 2 aqui.

Aqui está o código completo para o `package.xml` do pacote `my_py_pkg` *(também disponível [**nesse link**](https://github.com/fabiobento/cont-int-2026-1/blob/main/topics-ros2/scripts/my_py_pkg/package.xml))*:
```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>my_py_pkg</name>
  <version>0.0.0</version>
  <description>TODO: Package description</description>
  <maintainer email="todo.todo@todo.com">ed</maintainer>
  <license>TODO: License declaration</license>

  <depend>rclpy</depend>
  <depend>example_interfaces</depend>

  <test_depend>ament_copyright</test_depend>
  <test_depend>ament_flake8</test_depend>
  <test_depend>ament_pep257</test_depend>
  <test_depend>python3-pytest</test_depend>

  <export>
    <build_type>ament_python</build_type>
  </export>
</package>
```

Para instalar o nó, abra o arquivo `setup.py` do pacote `my_py_pkg` e adicione uma nova linha para criar outro executável:

```python
entry_points={
    'console_scripts': [
        "test_node = my_py_pkg.my_first_node:main",
        "number_publisher = my_py_pkg.number_publisher:main"
    ],
},
```

Certifique-se de adicionar uma vírgula entre cada linha; caso contrário, você poderá encontrar alguns erros estranhos ao compilar o pacote.


Aqui, criamos um novo executável chamado `number_publisher`.

> **Observação**
>
> Desta vez, como você pode ver neste exemplo, o nome do nó, o nome do arquivo e o nome do executável são os mesmos: `number_publisher`. Esta é uma prática comum de se fazer. Apenas lembre-se de que esses nomes representam três coisas diferentes.

Aqui está o código completo do `setup.py` *(também disponível [**nesse link**](https://github.com/fabiobento/cont-int-2026-1/blob/main/topics-ros2/scripts/my_py_pkg/setup.py))*:
```python
from setuptools import find_packages, setup

package_name = 'my_py_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ed',
    maintainer_email='todo.todo@todo.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "test_node = my_py_pkg.my_first_node:main",
            "number_publisher = my_py_pkg.number_publisher:main",      
        ],
    },
)
```

Agora, vá para o diretório raiz do seu workspace e compile o pacote `my_py_pkg`:

```bash
cd ~/master_ros2_ws/
colcon build --packages-select my_py_pkg --symlink-install
```
Usamos `--symlink-install` para que não precisemos rodar o `colcon build` toda vez que modificarmos o nó `number_publisher`.

**Executando o publicador**

Após o pacote ter sido compilado com sucesso, faça o *source* do seu *workspace* e inicie o nó:

```bash
source ~/.bashrc
ros2 run my_py_pkg number_publisher
[INFO] [1773082036.235805556] [number_publisher]: O publicador de números foi iniciado
```

O nó está rodando, mas além do log inicial, nada é exibido. Isso é normal — não pedimos para o nó imprimir mais nada.

Como sabemos que o publicador está funcionando? Poderíamos escrever um nó assinante agora mesmo e ver se recebemos as mensagens. Mas, antes de fazermos isso, podemos testar o publicador diretamente do Terminal.

Abra uma nova janela de Terminal e liste todos os tópicos:

```bash
ros2 topic list
/number
/parameter_events
/rosout
```

Aqui, você pode encontrar o tópico `/number`.

> **Observação:**
>
>Como você pode ver, há uma barra inicial adicionada à frente do nome do tópico. Nós escrevemos apenas `number` no código, não `/number`. Isso ocorre porque os nomes no ROS 2 (nós, tópicos e assim por diante) são organizados em *namespaces* (espaços de nomes). Mais tarde, veremos que você pode adicionar um *namespace* para colocar todos os seus tópicos ou nós dentro do *namespace* `/abc`, por exemplo. Neste caso, o nome do tópico seria `/abc/number`. Aqui, como nenhum *namespace* é fornecido, uma barra inicial é adicionada ao nome, mesmo que não a tenhamos fornecido no código. Poderíamos chamar isso de *namespace* global.

Com o comando `ros2 topic echo <nome_do_topico>`, você pode assinar o tópico diretamente pelo Terminal e ver o que está sendo publicado. Aprenderemos mais sobre este comando mais adiante:

```bash
ros2 topic echo /number
data: 2
---
data: 2
---
```

Como você pode ver, recebemos uma nova mensagem por segundo, que contém um campo `data` com o valor `2`. Isso é exatamente o que queríamos fazer no código.

Com isso, terminamos nosso primeiro publicador em Python. Vamos mudar para C++.

> **Observação:**
>
> "Na Engenharia, nós nunca conectamos a saída de um sistema à entrada de outro sem antes medir o sinal com um osciloscópio ou multímetro. O comando `ros2 topic echo` é o nosso 'multímetro virtual'. Ele permite validar se o sinal (os dados) está sendo gerado corretamente pelo publicador antes de perdermos tempo tentando debugar o código do assinante (o controlador)."

### **Escrevendo um publicador em C++**

Aqui, o processo é o mesmo que para o Python. Vamos criar um novo nó e, neste nó, adicionar um publicador e um temporizador (*timer*). Na função de *callback* do temporizador, criaremos uma mensagem e a publicaremos.

Vou passar um pouco mais rápido por esta seção, pois as explicações lógicas são as mesmas. Focaremos apenas nas especificidades da sintaxe do C++ com o ROS 2.

> **Observação**
>
> Para tudo relacionado a C++ neste material, certifique-se de acompanhar as explicações usando o código no GitHub em uma janela ao lado. Posso não fornecer o código completo aqui no texto, apenas os trechos importantes que são importantes para você entender. *(Nota: O código completo estará no repositório da disciplina).*

**Criando um nó com um publicador e um temporizador**

Primeiro, vamos criar um novo arquivo para o nosso nó `number_publisher` no pacote `my_cpp_pkg`:

```bash
cd ~/master_ros2_ws/src/my_cpp_pkg/src/
touch number_publisher.cpp
```

Abra este arquivo e escreva o código para o nó. Você pode começar a partir do [template de Programação Orientada a Objetos (POO)](https://github.com/fabiobento/cont-int-2026-1/blob/main/nodes-ros2/scripts/node_oop_template/node_oop_template.cpp) e adicionar o publicador, o temporizador e a função de *callback*.

Vou agora comentar sobre algumas linhas importantes:

```cpp
#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/msg/int64.hpp"

```

Para incluir uma interface para um tópico em C++, use `"<nome_do_pacote>/msg/<nome_da_mensagem>.hpp"`. Note que o nome do arquivo da mensagem fica em letras minúsculas.

Em seguida, no construtor, adicione o seguinte:

```cpp
number_publisher_ = this->create_publisher<example_interfaces::msg::Int64>("number", 10);

```

Em C++, também usamos o método `create_publisher()` da classe `Node`. A sintaxe é um pouco diferente, pois utiliza *templates* (`< >`), mas você ainda pode identificar a interface do tópico, o nome do tópico e o tamanho da fila (como lembrete, você pode defini-lo como `10` todas as vezes por enquanto).

O publicador também é declarado como um atributo privado na classe:

```cpp
rclcpp::Publisher<example_interfaces::msg::Int64>::SharedPtr number_publisher_;

```

Como você pode ver, usamos a classe `rclcpp::Publisher` e, como em muitas coisas no ROS 2, usamos um ponteiro inteligente compartilhado (*shared pointer*). Para várias classes comuns, o ROS 2 fornece o `::SharedPtr`, o que seria a mesma coisa que escrever `std::shared_ptr<o_publicador>`.

Vamos voltar ao construtor:

```cpp
number_timer_ = this->create_wall_timer(std::chrono::seconds(1), std::bind(&NumberPublisherNode::publishNumber, this));
RCLCPP_INFO(this->get_logger(), "Number publisher has been started.");

```

Após criar o publicador, criamos um temporizador para chamar o método `publishNumber` a cada `1.0` segundo. Por fim, imprimimos um log para sabermos que o código do construtor foi executado com sucesso.

```cpp
void publishNumber(){
    auto msg = example_interfaces::msg::Int64();
    msg.data = number_;
    number_publisher_->publish(msg);
}

```

Este é o método de *callback*. Assim como no Python, criamos um objeto a partir da classe da interface, preenchemos qualquer campo desta interface (no caso, `data`) e publicamos a mensagem.

Aqui está o código completo para esse nó publicador em C++ *(também disponível [**nesse link**](https://github.com/fabiobento/cont-int-2026-1/blob/main/topics-ros2/scripts/my_cpp_pkg/src/number_publisher.cpp))*:

```cpp
#include "example_interfaces/msg/int64.hpp"
#include "rclcpp/rclcpp.hpp"

class NumberPublisherNode : public rclcpp::Node {
public:
  NumberPublisherNode() : Node("number_publisher") {
    number_ = 2;
    number_publisher_ =
        this->create_publisher<example_interfaces::msg::Int64>("number", 10);
    number_timer_ = this->create_wall_timer(
        std::chrono::seconds(1),
        std::bind(&NumberPublisherNode::publishNumber, this));
    RCLCPP_INFO(this->get_logger(), "Number publisher has been started.");
  }

private:
  void publishNumber() {
    auto msg = example_interfaces::msg::Int64();
    msg.data = number_;
    number_publisher_->publish(msg);
  }

  int number_;
  rclcpp::Publisher<example_interfaces::msg::Int64>::SharedPtr
      number_publisher_;
  rclcpp::TimerBase::SharedPtr number_timer_;
};

int main(int argc, char **argv) {
  rclcpp::init(argc, argv);
  auto node = std::make_shared<NumberPublisherNode>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
```

**Compilando e executando o publicador**

Uma vez que você tenha escrito o nó com o publicador, temporizador e função de *callback*, é hora de compilá-lo.

Como fizemos para o Python, abra o arquivo `package.xml` do pacote `my_cpp_pkg` e adicione uma linha para a dependência ao `example_interfaces`:

```xml
<depend>rclcpp</depend>
<depend>example_interfaces</depend>

```

Aqui está o código completo para o `package.xml` do pacote `my_cpp_pkg` *(também disponível [**nesse link**](https://github.com/fabiobento/cont-int-2026-1/blob/main/topics-ros2/scripts/my_cpp_pkg/package.xml))*:

```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>my_cpp_pkg</name>
  <version>0.0.0</version>
  <description>TODO: Package description</description>
  <maintainer email="todo.todo@todo.com">ed</maintainer>
  <license>TODO: License declaration</license>

  <buildtool_depend>ament_cmake</buildtool_depend>

  <depend>rclcpp</depend>
  <depend>example_interfaces</depend>

  <test_depend>ament_lint_auto</test_depend>
  <test_depend>ament_lint_common</test_depend>

  <export>
    <build_type>ament_cmake</build_type>
  </export>
</package>

```

Em seguida, abra o arquivo `CMakeLists.txt` do pacote `my_cpp_pkg` e adicione as seguintes linhas:

```cmake
find_package(rclcpp REQUIRED)
find_package(example_interfaces REQUIRED)

add_executable(number_publisher src/number_publisher.cpp)
ament_target_dependencies(number_publisher rclcpp example_interfaces)

install(TARGETS
  number_publisher
  DESTINATION lib/${PROJECT_NAME}/
)

```

Para qualquer nova dependência de mensagem, precisamos adicionar uma nova linha `find_package()`.

Em seguida, criamos um novo executável. Note que também fornecemos `example_interfaces` nos argumentos de `ament_target_dependencies()`. Se você omitir isso, o vinculador (linker) do C++ falhará e você receberá um erro durante a compilação.

Por fim, não há necessidade de recriar o bloco `install()`. Apenas adicione o nome do novo executável em uma nova linha dentro dele, **sem vírgulas** entre as linhas (diferente do Python).

Aqui está o código completo para o `CMakeLists.txt` do pacote `my_cpp_pkg` *(também disponível [**nesse link**](https://github.com/fabiobento/cont-int-2026-1/blob/main/topics-ros2/scripts/my_cpp_pkg/package.xml)):

```cmake
cmake_minimum_required(VERSION 3.8)
project(my_cpp_pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(example_interfaces REQUIRED)

add_executable(test_node src/my_first_node.cpp)
ament_target_dependencies(test_node rclcpp)

add_executable(number_publisher src/number_publisher.cpp)
ament_target_dependencies(number_publisher rclcpp example_interfaces)

install(TARGETS
 test_node
 number_publisher
 DESTINATION lib/${PROJECT_NAME}/
)

ament_package()

```

Agora, você pode compilar, carregar as variáveis de ambiente (*source*) e executar:

```bash
cd ~/master_ros2_ws/
colcon build --packages-select my_cpp_pkg
source ~/.bashrc
ros2 run my_cpp_pkg number_publisher
[INFO] [1711528108.225880935] [number_publisher]: O publicador de números foi iniciado.

```

O nó contendo o publicador está ativo e rodando. Usando os comandos `ros2 topic list` e `ros2 topic echo /number` em outro terminal, você pode encontrar o tópico e ver o que está sendo publicado em tempo real.

Agora que você criou um publicador em C++ e sabe que ele está funcionando, é hora de aprender como criar um assinante (*subscriber*) para esse tópico.

## **Escrevendo um assinante de tópico**

Para continuar melhorando nossa aplicação, vamos criar um novo nó que assinará (*subscribe*) o tópico `/number`. Cada número recebido será adicionado a um contador. Queremos imprimir esse contador toda vez que ele for atualizado.

Como fizemos anteriormente, começaremos com as explicações completas em Python e, em seguida, veremos as especificidades da sintaxe em C++.

### **Escrevendo um assinante em Python**

Você pode encontrar o [código completo para este nó Python no GitHub](https://github.com/fabiobento/cont-int-2026-1/blob/main/topics-ros2/scripts/my_py_pkg/my_py_pkg/number_counter.py). Muitas coisas que precisamos fazer aqui são idênticas ao que fizemos anteriormente, então não vou detalhar cada passo. Em vez disso, focaremos nas partes mais importantes para escrevermos o assinante.

**Criando um nó Python com um assinante**

Crie um novo nó chamado `number_counter` dentro do pacote `my_py_pkg`:

```bash
cd ~/master_ros2_ws/src/my_py_pkg/my_py_pkg/
touch number_counter.py
chmod +x number_counter.py
```

Neste arquivo, você pode escrever o código para o nó e adicionar um assinante. Aqui está a explicação, passo a passo:

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64
```

Como queremos criar um assinante para receber o que enviamos com o publicador, precisamos usar a mesma interface. Portanto, também importamos `Int64`.

Em seguida, podemos criar o assinante:

```python
class NumberCounterNode(Node):
    def __init__(self):
        super().__init__("number_counter")
        self.counter_ = 0
        self.number_subscriber_ = self.create_subscription(Int64, "number", self.callback_number, 10)
        self.get_logger().info("Number Counter has been started.")

```

Assim como para os publicadores, criaremos os assinantes no construtor do nó. Aqui, usamos o método `create_subscription()` da classe `Node`. Com este método, você precisa fornecer quatro argumentos:

1. **Interface do tópico:** `Int64`. Esta precisa ser a mesma tanto para o publicador quanto para o assinante.
2. **Nome do tópico:** `number`. Este é o mesmo nome usado no publicador. Note que não forneço nenhuma barra adicional aqui. Ela será adicionada automaticamente, então o nome do tópico se tornará `/number`.
3. **Função de *callback*:** Lembra quando eu disse que quase tudo é um *callback* no ROS 2? Usamos um método de *callback* para o assinante aqui também. Quando o nó está em execução (*spinning*), ele permanecerá ativo e todos os *callbacks* registrados estarão prontos para serem chamados. Sempre que uma mensagem for publicada no tópico `/number`, ela será recebida aqui, e poderemos usá-la e processá-la dentro do método de *callback* (que precisamos implementar).
4. **Tamanho da fila (*Queue size*):** Como visto anteriormente, você pode defini-lo como `10` e não se preocupar com isso por enquanto.

Agora, vamos ver a implementação do método de *callback*, que nomeei como `callback_number`:

**Observação**
Como boa prática, recomendo nomear os métodos de *callback* para tópicos como `callback_<nome_do_topico>`. Ao adicionar o prefixo `callback_`, você deixa claro que este método é um *callback* e não deve ser chamado diretamente no seu código. Isso pode evitar muitos erros no futuro.

```python
    def callback_number(self, msg: Int64):
        self.counter_ += msg.data
        self.get_logger().info("Counter:  " + str(self.counter_))

```

Em um *callback* de assinante, você recebe a mensagem diretamente nos parâmetros da função. Como sabemos que `Int64` contém um campo `data`, podemos acessá-lo usando `msg.data`.

Agora, adicionamos o número recebido a um atributo `counter_` e imprimimos o contador toda vez com um log do ROS 2.

> **Observação**
>
> Como boa prática, especifiquei o tipo `Int64` para o argumento `msg` do método. Isso não é obrigatório para que o código Python funcione, mas adiciona um nível extra de segurança (temos certeza de que devemos receber um `Int64` e nada mais) e, às vezes, pode fazer com que o preenchimento automático (*auto-completion*) da sua IDE funcione melhor.

Para finalizar o nó, não se esqueça de adicionar a função padrão `main()` após a classe `NumberCounterNode`.

Aqui está o código completo para o nó assinante em Python *(também disponível [**nesse link**](https://github.com/fabiobento/cont-int-2026-1/blob/main/topics-ros2/scripts/my_py_pkg/my_py_pkg/number_counter.py))*:
```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64


class NumberCounterNode(Node):
    def __init__(self):
        super().__init__("number_counter")
        self.counter_ = 0
        self.number_subscriber_ = self.create_subscription(Int64, "number", self.callback_number, 10)
        self.get_logger().info("Contagem de números iniciada.")

    def callback_number(self, msg: Int64):
        self.counter_ += msg.data
        self.get_logger().info("Contador:  " + str(self.counter_))


def main(args=None):
    rclpy.init(args=args)
    node = NumberCounterNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
``` 


**Executando o assinante em Python**

Agora, para testar o código, adicione um novo executável ao arquivo `setup.py` do seu pacote Python:

```python
    entry_points={
        'console_scripts': [
            "test_node = my_py_pkg.my_first_node:main",
            "number_publisher = my_py_pkg.number_publisher:main",
            "number_counter = my_py_pkg.number_counter:main"
        ],
    },
```

Aqui o código completo do `setup.py`(também disponível [**nesse link**](https://github.com/fabiobento/cont-int-2026-1/blob/main/topics-ros2/scripts/my_py_pkg/setup.py)):
```python
from setuptools import find_packages, setup

package_name = 'my_py_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ed',
    maintainer_email='todo.todo@todo.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "test_node = my_py_pkg.my_first_node:main",
            "number_publisher = my_py_pkg.number_publisher:main",
            "number_counter = my_py_pkg.number_counter:main"
        ],
    },
)
```

Em seguida, compile o pacote e carregue as variáveis do *workspace* (daqui em diante, não escreverei esses comandos toda vez, pois são sempre os mesmos).

Agora, execute cada nó (`number_publisher` e `number_counter`) em um Terminal diferente:

```bash
ros2 run my_py_pkg number_publisher
[INFO] [1711529824.816514561] [number_publisher]: Number publisher has been started.

ros2 run my_py_pkg number_counter
[INFO] [1711528797.363370081] [number_counter]: Number Counter has been started.
[INFO] [1711528815.739270510] [number_counter]: Counter:  2
[INFO] [1711528816.739186942] [number_counter]: Counter:  4
[INFO] [1711528817.739050485] [number_counter]: Counter:  6
[INFO] [1711528818.738992607] [number_counter]: Counter:  8

```

Como você pode ver, o nó `number_counter` adiciona `2` ao contador a cada `1.0` segundo. Se você vir isso, significa que a comunicação de publicação/assinatura entre seus dois nós está funcionando perfeitamente.

Você pode parar e iniciar o nó `number_publisher` e verá que toda vez que você o iniciar, o `number_counter` continuará a somar os números a partir da contagem atual.

### **Escrevendo um assinante em C++**

Vamos criar o nó `number_counter` em C++. O princípio é o mesmo, então vamos focar apenas na sintaxe aqui.

**Criando um nó C++ com um assinante**

Crie um novo arquivo para o seu nó:

```bash
cd ~/master_ros2_ws/src/my_cpp_pkg/src/
touch number_counter.cpp
```

Abra este arquivo e escreva o código para o nó (mais uma vez, [o código completo](https://github.com/fabiobento/cont-int-2026-1/blob/main/topics-ros2/scripts/my_cpp_pkg/src/number_counter.cpp) estará no repositório da disciplina no GitHub).

Para criar um assinante em seu nó, use o seguinte código no construtor:

```cpp
number_subscriber_ = this->create_subscription<example_interfaces::msg::Int64>(
           "number",
           10,
           std::bind(&NumberCounterNode::callbackNumber, this, std::placeholders::_1));
```

Encontramos os mesmos componentes do Python (mas em uma ordem diferente): interface do tópico, nome do tópico, tamanho da fila e o *callback* para as mensagens recebidas. Para que o `_1` funcione, não se esqueça de adicionar `using namespace std::placeholders;` antes dele.

**Observação**
Mesmo que as bibliotecas `rclpy` e `rclcpp` devam ser baseadas no mesmo código , ainda pode haver algumas diferenças na API. Não se preocupe se o código às vezes não parecer o mesmo entre Python e C++.

O objeto assinante é declarado como um atributo privado:

```cpp
rclcpp::Subscription<example_interfaces::msg::Int64>::SharedPtr number_subscriber_;
```

Usamos a classe `rclcpp::Subscription` aqui e, mais uma vez, criamos um ponteiro compartilhado (*shared pointer*) para esse objeto.

Temos então o método de *callback*, `callbackNumber`:

```cpp
void callbackNumber(const example_interfaces::msg::Int64::SharedPtr msg)
{
    counter_ += msg->data;
    RCLCPP_INFO(this->get_logger(), "Counter: %d", counter_);
}
```

A mensagem que recebemos no *callback* também é um ponteiro compartilhado (constante). Portanto, **não se esqueça de usar `->**` em vez do ponto `.` ao acessar o campo `data`.

Neste *callback*, adicionamos o número recebido ao contador e o imprimimos.

Aqui está o código completo para o assinante em C++ *(também disponível [**nesse link**](https://github.com/fabiobento/cont-int-2026-1/blob/main/topics-ros2/scripts/my_cpp_pkg/src/number_counter.cpp))*:

```cpp
#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/msg/int64.hpp"

using namespace std::placeholders;

class NumberCounterNode : public rclcpp::Node
{
public:
    NumberCounterNode() : Node("number_counter"), counter_(0)
    {
        number_subscriber_ = this->create_subscription<example_interfaces::msg::Int64>(
                "number", 10, std::bind(&NumberCounterNode::callbackNumber, this, _1));
            
        RCLCPP_INFO(this->get_logger(), "Number Counter has been started.");
    }

private:
    void callbackNumber(const example_interfaces::msg::Int64::SharedPtr msg)
    {
        counter_ += msg->data;
        RCLCPP_INFO(this->get_logger(), "Counter: %d", counter_);
    }

    int counter_;
    rclcpp::Subscription<example_interfaces::msg::Int64>::SharedPtr number_subscriber_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<NumberCounterNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
``` 

**Executando o assinante em C++**

Crie um novo executável para esse nó. Abra o `CMakeLists.txt` e adicione o seguinte código:

```cmake
add_executable(number_counter src/number_counter.cpp)
ament_target_dependencies(number_counter rclcpp example_interfaces)

install(TARGETS
  test_node
  number_publisher
  number_counter
  DESTINATION lib/${PROJECT_NAME}/
)
```

Aqui está o código fonte completo para o `CMakeLists.txt` *(também está disponível [**nesse link**](https://github.com/fabiobento/cont-int-2026-1/blob/main/topics-ros2/scripts/my_cpp_pkg/CMakeLists.txt))*:

```cmake
cmake_minimum_required(VERSION 3.8)
project(my_cpp_pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(example_interfaces REQUIRED)

add_executable(test_node src/my_first_node.cpp)
ament_target_dependencies(test_node rclcpp)

add_executable(number_publisher src/number_publisher.cpp)
ament_target_dependencies(number_publisher rclcpp example_interfaces)

add_executable(number_counter src/number_counter.cpp)
ament_target_dependencies(number_counter rclcpp example_interfaces)

install(TARGETS
 test_node
 number_publisher
 number_counter
 DESTINATION lib/${PROJECT_NAME}/
)

ament_package()
```

Em seguida, compile o pacote `my_cpp_pkg`, carregue o *workspace* e execute tanto o nó publicador quanto o nó assinante em Terminais diferentes. Você deve ver uma saída semelhante à que tivemos com o Python.

### **Executando os nós em Python e C++ juntos**

Acabamos de criar um publicador e um assinante tanto em Python quanto em C++. O tópico que utilizamos possui o mesmo nome (`number`) e a mesma interface (`example_interfaces/msg/Int64`).

Se o tópico é o mesmo, isso significa que você poderia iniciar o nó `number_publisher` em Python junto com o nó `number_counter` em C++, por exemplo.

Vamos verificar isso:

```bash
ros2 run my_py_pkg number_publisher
[INFO] [1711597703.615546913] [number_publisher]: Number publisher has been started.

ros2 run my_cpp_pkg number_counter
[INFO] [1711597740.879160448] [number_counter]: Number Counter has been started.
[INFO] [1711597741.607444197] [number_counter]: Counter: 2
[INFO] [1711597742.607408224] [number_counter]: Counter: 4

```

Você também pode tentar o inverso, executando o nó `number_publisher` em C++ com o nó `number_counter` em Python.

**Por que isso funciona?**

Simplesmente porque o ROS 2 é agnóstico em relação à linguagem. Você pode ter um nó escrito em qualquer linguagem de programação suportada, e esse nó poderá se comunicar com todos os outros nós da rede, utilizando tópicos e outras formas de comunicação do ROS 2.

As comunicações do ROS 2 ocorrem em um nível mais baixo, utilizando o *Data Distribution Service* (DDS). Esta é a camada de *middleware* responsável pelo envio e recebimento de mensagens entre os nós. Quando você escreve um nó em Python ou C++, está utilizando a mesma funcionalidade do DDS, apenas com uma API implementada em `rclpy` ou `rclcpp`.

Não vou me aprofundar muito nessa explicação, pois é um assunto bastante avançado. Se há apenas uma coisa para se lembrar de tudo isso, é que nós em Python e C++ podem se comunicar entre si perfeitamente usando os recursos do ROS 2. Você pode criar alguns nós em Python e outros em C++; basta garantir o uso do mesmo nome de comunicação e da mesma interface de ambos os lados.

##  **Ferramentas adicionais para lidar com tópicos**

Você acabou de escrever alguns nós contendo publicadores e assinantes. Agora, exploraremos como as ferramentas do ROS 2 podem ajudá-lo a fazer mais coisas com os tópicos.

> Exploraremos os seguintes tópicos:
> 
> * Introspecção com `rqt_graph`
> * Introspecção e depuração com a linha de comando `ros2 topic`
> * Alteração do nome de um tópico ao iniciar um nó
> * Reprodução de dados de tópicos com bags (*ROS 2 bags*)



### **Introspecção de tópicos com rqt_graph**

Nós usamos o `rqt_graph` para visualizar os nós na Aula 1. Vamos executá-lo novamente e ver como inspecionar o publicador e o assinante que acabamos de criar.

Primeiro, inicie ambos os nós `number_publisher` e `number_counter` (de qualquer pacote: `my_py_pkg` ou `my_cpp_pkg`).

Em seguida, inicie o `rqt_graph` em outro Terminal:

```bash
rqt_graph
```
> **Observação**
>
> Após executar o `rqt_graph` você possivelmente precisará clicar em `
Refresh ROS Graph` para que o gráfico seja atualizado.

Se necessário, atualize a visualização algumas vezes e selecione `Nodes/Topics (all)`. Você também pode desmarcar a caixa `Dead sinks` e a caixa `Leaf topics`. Isso permitirá que você veja os tópicos mesmo se houver apenas um assinante e nenhum publicador, ou um publicador e nenhum assinante:


![](https://github.com/fabiobento/cont-int-2026-1/raw/main/topics-ros2/imagens/topics-rqt.png)
**O tópico `number` no rqt_graph** (Fonte: O autor, gerado via `rqt_graph`)

Lá, podemos ver o nó `number_publisher` e o nó `number_counter`. No meio, temos o tópico `/number`, e podemos ver qual nó é um publicador ou um assinante.

O pacote `rqt_graph` pode ser extremamente útil ao depurar tópicos. Imagine que você executa alguns nós e se pergunta por que as mensagens do tópico não são recebidas por um assinante. Talvez esses nós não estejam usando o mesmo nome de tópico. Você pode ver isso facilmente com o `rqt_graph`:

![](https://github.com/fabiobento/cont-int-2026-1/raw/main/topics-ros2/imagens/topics-rqt-error.png)
**Incompatibilidade de nome de tópico entre publicador e assinante** ([Fonte](https://www.packtpub.com/en-us/product/ros-2-from-scratch-9781835881415))

Neste exemplo, foi cometido um erro intencional no nome do tópico dentro do publicador. Em vez de `number`, escreveu-se `numberr`. Com o `rqt_graph`, posso ver onde está o problema. Os dois nós não estão se comunicando um com o outro.


### **A linha de comando ros2 topic**

Com o `ros2 node`, obtemos ferramentas de linha de comando adicionais para os nós. Para os tópicos, usaremos o `ros2 topic`.

Se você executar `ros2 topic -h`, verá que há muitos comandos. Você já conhece alguns deles. Aqui, farei uma rápida recapitulação e explorarei mais alguns comandos que podem ser úteis ao depurar tópicos.

Primeiro, para listar todos os tópicos, use `ros2 topic list`:

```bash
ros2 topic list
/number
/parameter_events
/rosout

```

Como você pode ver, obtemos o tópico `/number`. Você também sempre obterá `/parameter_events` e `/rosout` (todos os logs do ROS 2 são publicados neste tópico).

Com `ros2 topic info <nome_do_topico>`, você pode obter a interface do tópico, bem como o número de publicadores e assinantes para aquele tópico:

```bash
ros2 topic info /number
Type: example_interfaces/msg/Int64
Publisher count: 1
Subscription count: 1

```

Então, para ir mais longe e ver os detalhes da interface, você pode executar o seguinte comando:

```bash
ros2 interface show example_interfaces/msg/Int64
# alguns comentários
int64 data

```

Com isso, temos todas as informações de que precisamos para criar um publicador ou assinante adicional para o tópico.

Além disso, também podemos assinar o tópico diretamente pelo Terminal com `ros2 topic echo <nome_do_topico>`. Foi o que fizemos logo após escrever o publicador para garantir que ele estivesse funcionando antes de escrevermos qualquer assinante:

```bash
ros2 topic echo /number
data: 2
---
data: 2
---

```

Por outro lado, você pode publicar em um tópico diretamente pelo Terminal com `ros2 topic pub -r <frequência> <nome_do_topico> <interface> <mensagem_em_json>`. Para testar isso, pare todos os nós e inicie apenas o nó `number_counter` em um Terminal. Além do log inicial, nada será impresso. Em seguida, execute o seguinte comando em outro Terminal:

```bash
ros2 topic pub -r 2.0 /number example_interfaces/msg/Int64 "{data: 7}"
publisher: beginning loop
publishing #1: example_interfaces.msg.Int64(data=7)
publishing #2: example_interfaces.msg.Int64(data=7)

```

Isso publicará no tópico `/number` a `2.0` Hertz (a cada `0.5` segundos). Ao executar isso, você verá alguns logs no nó `number_counter`, o que significa que as mensagens foram recebidas:

```bash
[INFO] [1711600360.459298369] [number_counter]: Counter: 7
[INFO] [1711600360.960216275] [number_counter]: Counter: 14
[INFO] [1711600361.459896877] [number_counter]: Counter: 21

```

Dessa forma, você pode testar um assinante sem precisar escrever um publicador primeiro. Note que isso só funciona bem para tópicos com uma interface simples. Quando a interface contém muitos campos, torna-se muito complicado escrever tudo no Terminal.

**Observação**
Tanto o `ros2 topic echo` quanto o `ros2 topic pub` podem economizar muito tempo, e isso também é ótimo para colaborar com outras pessoas em um projeto. Você poderia ser responsável por escrever um publicador, e outra pessoa escreveria um assinante. Com essas ferramentas de linha de comando, ambos podem garantir que a comunicação do tópico esteja funcionando. Assim, quando vocês executarem os dois nós juntos, saberão que os dados enviados ou recebidos estão corretos.


### **Reproduzindo dados de tópicos com bags**

Imagine este cenário: você está trabalhando em um robô móvel que deve ter um determinado desempenho ao navegar do lado de fora enquanto está chovendo.

Isso significa que você precisará executar o robô nessas condições para poder desenvolver sua aplicação. Há alguns problemas: talvez você não tenha acesso ao robô o tempo todo, ou não possa levá-lo para fora, ou simplesmente não chove todo dia.

Uma solução para isso é usar bags (*ROS 2 bags*). Os bags permitem que você grave um tópico e o reproduza mais tarde. Assim, você pode executar o experimento uma vez com as condições necessárias e, em seguida, reproduzir os dados exatamente como foram gravados. Com esses dados em loop, você pode desenvolver a sua aplicação de controle no conforto do laboratório.

Vamos considerar outro cenário comum em Sistemas Embarcados: você trabalha com um hardware (um sensor ultrassônico ou uma IMU) que ainda não está estável. Na maior parte do tempo, ele não funciona corretamente. Você poderia gravar um bag enquanto o hardware estiver funcionando bem e, em seguida, reproduzir esse bag para desenvolver sua aplicação de controle em vez de tentar usar o hardware de novo e de novo e perder tempo com as falhas dele.

Para trabalhar com bags no ROS 2, você deve usar a ferramenta de linha de comando `ros2 bag`. Vamos aprender como salvar e reproduzir um tópico com bags.

Primeiro, pare todos os nós e execute apenas o nó `number_publisher`.

Já sabemos que o nome do tópico é `/number`. Você pode recuperar isso com `ros2 topic list` se necessário. Em seguida, em outro Terminal, grave o bag com `ros2 bag record <lista_de_topicos> -o <nome_do_bag>`. Para deixar as coisas mais organizadas, sugiro que você crie uma pasta `bags` e grave de dentro dessa pasta:

```bash
mkdir ~/bags
cd ~/bags/
ros2 bag record /number -o bag1
...
[INFO] [1711602240.190476880] [rosbag2_recorder]: Subscribed to topic '/number'
[INFO] [1711602240.190542569] [rosbag2_recorder]: Recording...
[INFO] [1711602240.190729185] [rosbag2_recorder]: All requested topics are subscribed. Stopping discovery...

```

Neste ponto, o bag está gravando e salvando todas as mensagens recebidas dentro de um banco de dados. Deixe-o rodar por alguns segundos e, em seguida, pare-o com `Ctrl + C`:

```bash
[INFO] [1711602269.786924027] [rosbag2_cpp]: Writing remaining messages from cache to the bag. It may take a while
[INFO] [1711602269.787416646] [rosbag2_recorder]: Event publisher thread: Exiting
[INFO] [1711602269.787547010] [rosbag2_recorder]: Recording stopped

```

O comando `ros2 bag` será encerrado e você terminará com um novo diretório chamado `bag1`. Neste diretório, você encontrará um arquivo `.mcap` contendo as mensagens gravadas e um arquivo YAML com mais informações. Se você abrir este arquivo YAML, verá a duração da gravação, o número de mensagens gravadas e os tópicos que foram gravados.

Agora, você pode reproduzir o bag, o que significa que ele publicará no tópico exatamente como foi feito durante a gravação.

Pare o nó `number_publisher` (pois não queremos dados falsos se misturando com a gravação) e reproduza o bag com `ros2 bag play <caminho_para_o_bag>`:

```bash
ros2 bag play ~/bags/bag1/
```

Isso publicará todas as mensagens gravadas, com a mesma duração da gravação. Então, se você gravou por 3 minutos e 14 segundos, o bag reproduzirá o tópico por 3 minutos e 14 segundos. Depois disso, o bag será encerrado, e você poderá reproduzi-lo novamente se quiser.

Enquanto o bag estiver sendo reproduzido, você pode executar seu(s) assinante(s). Você pode fazer um teste rápido com `ros2 topic echo /number` e ver os dados passando. Você também pode executar seu nó `number_counter`, e verá que as mensagens são recebidas como se o sensor real estivesse lá.

Você agora é capaz de salvar e reproduzir um tópico usando os bags do ROS 2. Você pode explorar opções mais avançadas usando `ros2 bag -h`.

Como você viu, existem várias ferramentas disponíveis para lidar com tópicos. Use essas ferramentas com a maior frequência possível para inspecionar, depurar e testar seus tópicos. Elas pouparão muito do seu tempo ao desenvolver sua aplicação de controle no ROS 2.

Estamos quase terminando com os tópicos. Até agora, tudo o que fizemos foi usar interfaces (*messages*) existentes. A seguir, vamos aprender como criar uma interface de dados personalizada.

> **Observação**
>
> É exatamente assim que se trabalha com *Machine Learning* e *MLOps* aplicado à robótica. O fluxo de trabalho padrão da indústria é colocar o robô em operação, usar o `ros2 bag record` para gravar os dados dos sensores (câmera, lidar, posição), e depois usar esse `.mcap` gravado para treinar as redes neurais e algoritmos genéticos *offline*, garantindo que os dados de treino reflitam as condições reais do hardware.

## **Criando uma interface personalizada para um tópico**

Ao criar um publicador (*publisher*) ou assinante (*subscriber*) para um tópico, você sabe que precisa usar um nome e uma interface.

É bem fácil publicar ou assinar um tópico existente: você encontra o nome e a interface usando a linha de comando `ros2` e usa isso no seu código.

Agora, se você quiser iniciar um publicador ou assinante para um novo tópico, precisará escolher um nome e uma interface por conta própria:

* **Nome:** Sem problemas — é apenas uma cadeia de caracteres.
* **Interface:** Você tem duas opções — usar uma interface existente que funcione com o seu tópico ou criar uma nova.

Vamos tentar aplicar a filosofia do ROS 2 de não reinventar a roda. Ao criar um novo tópico, verifique se há alguma interface existente que atenda às suas necessidades. Se houver, use-a; não a recrie.

Primeiro, você aprenderá onde encontrar interfaces existentes. Depois, aprenderá como criar uma nova.

**Observação**
É bastante comum usar a palavra *mensagem* (*message*) quando falamos sobre interfaces de tópicos. Eu poderia ter nomeado esta seção como *Criando uma mensagem personalizada*. Na próxima seção, quando eu falar sobre mensagens, estarei me referindo a interfaces de tópicos.

### **Usando interfaces existentes**

Antes de iniciar um novo publicador ou assinante para um tópico, reserve um tempo para pensar sobre que tipo de dados você deseja enviar ou receber. Em seguida, verifique se uma interface já existente contém o que você precisa.

**Onde encontrar interfaces**

Assim como os nós, as interfaces são organizadas em pacotes. Você pode encontrar os pacotes mais comuns para interfaces do ROS 2 aqui: [https://github.com/ros2/common_interfaces](https://github.com/ros2/common_interfaces). Nem todas as interfaces existentes estão listadas aqui, mas já é bastante coisa. Para outras interfaces, uma simples pesquisa na internet deve levá-lo ao repositório correspondente no GitHub.

Neste repositório de interfaces comuns, você pode encontrar a mensagem `Twist` que usamos com o Turtlesim, dentro do pacote `geometry_msgs`. Como você pode ver, para interfaces de tópicos, temos então uma pasta adicional `msg`, que contém todas as definições de mensagens para aquele pacote.

Agora, digamos que você queira criar um nó de *driver* para uma câmera e publicar as imagens em um tópico. Se você olhar dentro do pacote `sensor_msgs` e, em seguida, dentro da pasta `msg`, encontrará um arquivo chamado `Image.msg`. Esta mensagem `Image` provavelmente é adequada para as suas necessidades. Ela também é usada por muitas outras pessoas, o que facilitará ainda mais a sua vida.

**Usando uma interface existente no seu código**

Para usar esta mensagem, certifique-se de ter instalado o pacote que a contém — neste caso, `sensor_msgs`. Como um lembrete rápido, para instalar um pacote ROS 2, você pode rodar `sudo apt install ros-<distro>-<nome_do_pacote>`:

```bash
sudo apt install ros-jazzy-sensor-msgs
```

Talvez o pacote já estivesse instalado. Caso contrário, carregue as variáveis do seu ambiente (*source*) novamente em seguida. Então, você pode encontrar os detalhes sobre a interface com `ros2 interface show <interface>`:

```bash
ros2 interface show sensor_msgs/msg/Image
```

Para usar esta mensagem no seu código, basta seguir o que fizemos neste capítulo (com a mensagem `example_interfaces/msg/Int64`):

1. No arquivo `package.xml` do pacote onde você escreve seus nós, adicione a dependência ao pacote da interface.
2. No seu código, importe a mensagem e use-a no seu publicador ou assinante.
3. **Apenas para C++:** Adicione a dependência ao pacote da interface no arquivo `CMakeLists.txt`.

Veremos outro exemplo deste processo muito em breve, logo após criarmos nossa própria interface.

Neste ponto, você sabe como encontrar e usar mensagens existentes no seu código. Mas você deve sempre fazer isso?

**Quando não usar mensagens existentes**

Para casos de uso comuns, sensores e atuadores, você provavelmente encontrará o que precisa. No entanto, se a interface não corresponder exatamente ao que você deseja, você terá que criar uma nova.

Existem alguns pacotes contendo interfaces básicas, como `example_interfaces` ou até mesmo `std_msgs`. Você pode se sentir tentado a usá-las no seu código real. Como melhor prática, é melhor evitar isso. Basta ler os comentários das definições dessas mensagens para ter certeza disso:

```bash
ros2 interface show example_interfaces/msg/Int64
# This is an example message of using a primitive datatype, int64.
# If you want to test with this that's fine, but if you are deploying it into a system you should create a semantically meaningful message type.
# If you want to embed it in another message, use the primitive data type instead.
int64 data

ros2 interface show std_msgs/msg/Int64
# This was originally provided as an example message.
# It is deprecated as of Foxy
# It is recommended to create your own semantically meaningful message.
# However if you would like to continue using this please use the equivalent in example_msgs.
int64 data

```

Como você pode ver, o pacote `std_msgs` está obsoleto (*deprecated*), e o pacote `example_interfaces` é recomendado apenas para fazer testes — que foi o que fizemos neste capítulo até agora para nos ajudar a aprender os vários conceitos de tópicos.

Como regra geral, se você não encontrar exatamente o que precisa nos pacotes de interfaces existentes, então crie a sua própria interface. Não é difícil de fazer e será sempre o mesmo processo.

### **Criando uma nova interface de tópico**

Você agora criará sua primeira interface personalizada para um tópico. Veremos como configurar um pacote para isso, como criar e compilar (*build*) a interface e como usá-la em nosso código.

**Criando e configurando um pacote de interfaces**

Antes de criarmos qualquer interface de tópico (mensagem), precisamos criar um novo pacote e configurá-lo para construir interfaces. Como boa prática, na sua aplicação, você terá **um pacote dedicado** a interfaces personalizadas. Isso significa que você cria interfaces apenas neste pacote e mantém este pacote apenas para interfaces — sem nós ou outras coisas, apenas interfaces. Isso tornará muito mais fácil quando você estiver escalando a aplicação e ajudará a evitar a criação de uma bagunça de dependências.

Uma prática comum ao nomear este pacote de interfaces é começar com o nome da sua aplicação ou robô e adicionar o sufixo `_interfaces`. Portanto, se o seu robô se chama `abc`, você deve usar `abc_interfaces`.

Não temos um robô para este exemplo, então vamos apenas nomear o pacote como `my_robot_interfaces`.

Crie um novo pacote com o tipo de build `ament_cmake` e sem dependências. Você nem precisa fornecer o tipo de build, pois o `ament_cmake` é o usado por padrão para C++ e criação de mensagens. Navegue até o diretório `src` do seu *workspace* e crie este pacote:

```bash
cd ~/master_ros2_ws/src/
ros2 pkg create my_robot_interfaces

```

Neste ponto, seu *workspace* deve conter três pacotes: `my_py_pkg`, `my_cpp_pkg` e `my_robot_interfaces`.

Precisamos configurar este novo pacote e modificar algumas coisas para que ele possa construir mensagens. Entre no pacote, remova os diretórios `src` e `include` (pois não escreveremos código C++ nele) e crie uma nova pasta `msg`:

```bash
cd my_robot_interfaces/
rm -r src/ include/
mkdir msg

```

Agora, abra o arquivo `package.xml` deste pacote. Após `<buildtool_depend>ament_cmake</buildtool_depend>`, adicione as seguintes três linhas. Recomendo que você simplesmente copie e cole para não cometer nenhum erro de digitação:

```xml
<build_depend>rosidl_default_generators</build_depend>
<exec_depend>rosidl_default_runtime</exec_depend>
<member_of_group>rosidl_interface_packages</member_of_group>

```

Com isso, o arquivo `package.xml` está completo e você não precisará fazer mais nada com ele por enquanto.

Aqui o arquivo `package.xml` completo *(também disponível **[nesse link](https://github.com/fabiobento/cont-int-2026-1/blob/main/topics-ros2/scripts/my_robot_interfaces/package.xml)**)*:
```cmake
# Define a versão mínima exigida do sistema de compilação CMake
cmake_minimum_required(VERSION 3.8)

# Define o nome do projeto (deve ser o mesmo nome contido no package.xml)
project(my_robot_interfaces)

# Adiciona flags de compilação rigorosas caso o compilador seja GCC ou Clang.
# Isso ativa vários alertas para manter e melhorar a qualidade do código.
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Busca os pacotes do ROS 2 dos quais este projeto depende
# ament_cmake: Essencial para construir e gerografar pacotes no padrão do ROS 2
find_package(ament_cmake REQUIRED)
# rosidl_default_generators: Pacote contendo as ferramentas para ler arquivos .msg/.srv/.action
# e gerar os respectivos códigos-fonte (em C++, Python, etc.) para sua utilização
find_package(rosidl_default_generators REQUIRED)

# Solicita ao sistema que processe as interfaces (mensagens) listadas e gere seus códigos
# É fundamental que o caminho inclua a pasta "msg/" antes do nome do arquivo
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/HardwareStatus.msg"
)

# Exporta as dependências necessárias para a infraestrutura de mensagens funcionar em tempo de execução
# Isso garante que quem importar suas mensagens de `my_robot_interfaces` terá acesso às dependências subjacentes
ament_export_dependencies(rosidl_default_runtime)

# Macro final obrigatória que processa todos os passos definidos e gera arquivos para os demais pacotes encontrarem este
ament_package()

```



Abra o arquivo `CMakeLists.txt`. Após `find_package(ament_cmake REQUIRED)` e antes de `ament_package()`, adicione as seguintes linhas (você também pode remover o bloco `if(BUILD_TESTING)`):

```cmake
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  # adicionaremos o nome das nossas interfaces personalizadas aqui depois
)

ament_export_dependencies(rosidl_default_runtime)

```

Não há muito o que entender sobre essas linhas que você está adicionando. Elas encontrarão algumas dependências (pacotes `rosidl`) e prepararão seu pacote para que ele possa construir interfaces.

O código fonte completo desse `CMakeLists.txt` *(também disponível **[nesse link](https://github.com/fabiobento/cont-int-2026-1/blob/main/topics-ros2/scripts/my_robot_interfaces/CMakeLists.txt)**)*:
```cmake
# Define a versão mínima exigida do sistema de compilação CMake
cmake_minimum_required(VERSION 3.8)

# Define o nome do projeto (deve ser o mesmo nome contido no package.xml)
project(my_robot_interfaces)

# Adiciona flags de compilação rigorosas caso o compilador seja GCC ou Clang.
# Isso ativa vários alertas para manter e melhorar a qualidade do código.
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Busca os pacotes do ROS 2 dos quais este projeto depende
# ament_cmake: Essencial para construir e gerografar pacotes no padrão do ROS 2
find_package(ament_cmake REQUIRED)
# rosidl_default_generators: Pacote contendo as ferramentas para ler arquivos .msg/.srv/.action
# e gerar os respectivos códigos-fonte (em C++, Python, etc.) para sua utilização
find_package(rosidl_default_generators REQUIRED)

# Solicita ao sistema que processe as interfaces (mensagens) listadas e gere seus códigos
# É fundamental que o caminho inclua a pasta "msg/" antes do nome do arquivo
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/HardwareStatus.msg"
)

# Exporta as dependências necessárias para a infraestrutura de mensagens funcionar em tempo de execução
# Isso garante que quem importar suas mensagens de `my_robot_interfaces` terá acesso às dependências subjacentes
ament_export_dependencies(rosidl_default_runtime)

# Macro final obrigatória que processa todos os passos definidos e gera arquivos para os demais pacotes encontrarem este
ament_package()

```

Neste ponto, seu pacote está pronto e você pode adicionar novas interfaces. Você só precisará fazer esta fase de configuração uma vez. Daqui para frente, adicionar uma nova interface será muito rápido.



### **Criando e construindo uma nova interface para um tópico**

Digamos que queremos criar um publicador para enviar algum tipo de status de hardware do nosso robô, incluindo a versão do robô, a temperatura interna, um sinalizador (flag) para saber se os motores estão prontos e uma mensagem de depuração.

Pesquisamos nas interfaces existentes e nada corresponde perfeitamente. Como você pode nomear esta nova interface? Aqui estão as regras que você deve seguir:

* **Use UpperCamelCase** — por exemplo, `HardwareStatus`.
* **Não escreva `Msg` ou `Interface` no nome**, pois isso adicionaria redundância desnecessária.
* **Use `.msg**` para a extensão do arquivo.

Seguindo essas regras, crie um novo arquivo chamado `HardwareStatus.msg` na pasta `msg`:

```bash
cd ~/master_ros2_ws/src/my_robot_interfaces/msg/
touch HardwareStatus.msg
```

Dentro deste arquivo, podemos adicionar a definição para a mensagem. Aqui está o que você pode usar:

* **Tipos embutidos (*Built-in types*)**, como `bool`, `byte`, `int64`, `float64` e `string`, bem como arrays desses tipos.
* **Outras mensagens existentes**, usando o nome do pacote, seguido pelo nome da mensagem — por exemplo, `geometry_msgs/Twist` (não adicione a pasta `msg` aqui).

Para simplificar as coisas, começaremos com apenas tipos embutidos. Escreva o seguinte dentro do arquivo da mensagem:

```msg
int64 version
float64 temperature
bool are_motors_ready
string debug_message

```

Para cada campo, fornecemos o tipo de dado e, em seguida, o nome do campo.

Agora, como vamos construir (*build*) esta mensagem? Como podemos obter uma classe Python ou C++ que possamos importar/incluir e usar no nosso código?

Para construir a mensagem, você simplesmente precisa adicionar uma linha ao `CMakeLists.txt`, especificando o caminho relativo para o arquivo da mensagem:

```cmake
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/HardwareStatus.msg"
)

```

Para cada nova interface que você construir neste pacote, você adicionará uma linha dentro da função `rosidl_generate_interfaces()`. **Não adicione vírgulas** entre as linhas.

O código fonte para o `CMakeLists.txt` é (*[disponível aqui](https://github.com/fabiobento/cont-int-2026-1/blob/main/topics-ros2/scripts/my_robot_interfaces/CMakeLists.txt)*):
```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<!-- Define a versão 3 do formato do pacote ROS 2 -->
<package format="3">
  <!-- Nome identificador do pacote no seu workspace -->
  <name>my_robot_interfaces</name>
  <version>0.0.0</version>
  <description>TODO: Package description</description>
  <maintainer email="todo.todo@todo.com">ed</maintainer>
  <license>TODO: License declaration</license>

  <!-- Declaração do sistema padrão de compilação do ROS 2 -->
  <buildtool_depend>ament_cmake</buildtool_depend>

  <!-- Dependência obrigatória na fase de compilação para processar e gerar o código a partir dos arquivos .msg/.srv -->
  <build_depend>rosidl_default_generators</build_depend>
  
  <!-- Dependência obrigatória na fase execução para as mensagens fluírem entre os nós corretamente -->
  <exec_depend>rosidl_default_runtime</exec_depend>
  
  <!-- Tag fundamental: Ela notifica todo o ambiente ROS 2 de que este pacote contém definições de interfaces -->
  <!-- Caso essa tag seja omitida, o ROS não conseguirá descobrir as suas mensagens -->
  <member_of_group>rosidl_interface_packages</member_of_group>

  <!-- Dependências automatizadas para garantir formatação e testes -->
  <test_depend>ament_lint_auto</test_depend>
  <test_depend>ament_lint_common</test_depend>

  <!-- Define que outras ferramentas de compilação devem tratar este pacote como um pacote C++ gerenciado pelo ament -->
  <export>
    <build_type>ament_cmake</build_type>
  </export>
</package>
```


Agora, salve todos os arquivos e compile o seu novo pacote:

```bash
cd ~/master_ros2_ws/
colcon build --packages-select my_robot_interfaces
Starting >>> my_robot_interfaces
Finished <<< my_robot_interfaces [4.00s]
Summary: 1 package finished [4.28s]

```

O sistema de build pegará a definição de interface que você escreveu e a usará para gerar o código-fonte automaticamente tanto para Python quanto para C++:


![](https://github.com/fabiobento/cont-int-2026-1/raw/main/topics-ros2/imagens/build-system-interface.jpg)
**Sistema de build para interfaces** ([Fonte](https://www.packtpub.com/en-us/product/ros-2-from-scratch-9781835881415))


Depois de compilar o pacote, certifique-se de carregar as variáveis do ambiente (*source*). Você deverá ser capaz de ver sua interface pelo Terminal (não se esqueça de usar o preenchimento automático com a tecla *Tab* para construir o comando mais rápido e ter certeza de que tem o nome correto):

```bash
source ~/.bashrc
ros2 interface show my_robot_interfaces/msg/HardwareStatus
int64 version
float64 temperature
bool are_motors_ready
string debug_message

```

Se você vir isso, significa que o processo de build foi bem-sucedido. Se você não conseguir ver a interface no Terminal, precisará voltar e verificar se fez todas as etapas corretamente (especialmente no `CMakeLists.txt`).

**Usando sua mensagem personalizada no seu código**

Digamos que você queira usar a sua nova interface no nó `number_publisher` que você criou nesta aula, dentro do pacote `my_py_pkg`.

Primeiro, abra o arquivo `package.xml` do pacote `my_py_pkg` e adicione uma dependência ao `my_robot_interfaces`:

```xml
<depend>rclpy</depend>
<depend>example_interfaces</depend>
<depend>my_robot_interfaces</depend>

```

Em seguida, para o **Python**, faça o seguinte:

Importe a mensagem adicionando a seguinte linha no topo do seu código:

```python
from my_robot_interfaces.msg import HardwareStatus

```

Ao criar o publicador, especifique a interface `HardwareStatus`.
Crie uma mensagem no seu código, preenchendo os campos assim:

```python
msg = HardwareStatus()
msg.temperature = 34.5
msg.version = 1
msg.are_motors_ready = True
msg.debug_message = "All systems go!"

```

O script `number_publisher.py` ficaria assim:
```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.msg import HardwareStatus


class NumberPublisherNode(Node):
    def __init__(self):
        # Mantive o nome do nó como "number_publisher" para evitar quebrar algo externo, 
        # mas você também pode mudar para "hardware_status_publisher" futuramente.
        super().__init__("number_publisher")
        
        # 1. Especificando a interface HardwareStatus ao criar o publicador
        self.hardware_status_publisher_ = self.create_publisher(HardwareStatus, "hardware_status", 10)        
        
        # O timer chama a função abaixo a cada 1 segundo para publicar a mensagem
        self.status_timer_ = self.create_timer(1.0, self.publish_hardware_status)
        self.get_logger().info("O publicador de status do hardware foi iniciado.")      

    def publish_hardware_status(self):
        # 2. Criando a mensagem e preenchendo os campos
        msg = HardwareStatus()
        msg.temperature = 34.5
        msg.version = 1
        msg.are_motors_ready = True
        msg.debug_message = "All systems go!"
        
        # 3. Publicando a mensagem na rede ROS 2
        self.hardware_status_publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = NumberPublisherNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
```

Você pode rodar o nó assim:
```bash
ros2 run my_py_pkg number_publisher 
```

E monitorar o tópico assim:
```bash
ros2 topic echo /hardware_status 
version: 1
temperature: 34.5
are_motors_ready: true
debug_message: All systems go!
---


**Observação para VS Code em Python:**
Se você estiver usando o VS Code, a mensagem pode não ser reconhecida e ficar sublinhada em vermelho após a importação. Feche o VS Code e abra-o novamente em um Terminal onde você já tenha feito o `source ~/.bashrc`.

Se você quiser usar esta mensagem no seu nó **C++** do pacote `my_cpp_pkg`:

1. Adicione a dependência ao `my_robot_interfaces` no arquivo `package.xml` e no `CMakeLists.txt` do `my_cpp_pkg`.
2. Importe a mensagem adicionando a seguinte linha de `#include` no seu código:

```cpp
#include "my_robot_interfaces/msg/hardware_status.hpp"

```

3. Crie um publicador e especifique a interface com `<my_robot_interfaces::msg::HardwareStatus>`.
4. Crie uma mensagem no seu código, assim:

```cpp
auto msg = my_robot_interfaces::msg::HardwareStatus();
msg.temperature = 34.5;
msg.are_motors_ready = true;

```

Você agora pode criar e usar a sua interface personalizada para tópicos. Como você viu, primeiro, verifique se há alguma interface existente que atenda às suas necessidades. Se houver, não reinvente a roda. Se nada se encaixar perfeitamente, no entanto, não hesite em criar sua própria interface. Para fazer isso, você deve criar um pacote novo dedicado a interfaces. Uma vez que você tenha terminado o processo de configuração para este pacote, você pode adicionar quantas interfaces quiser.

## **Desafio de Tópicos – controle em malha fechada**

Aqui está um desafio para você continuar praticando a criação de nós, publicadores e assinantes. Iniciaremos um novo projeto ROS 2 e o aprimoraremos ao longo das próximas aulas, à medida que descobrirmos mais conceitos.

Encorajo você a ler as instruções e reservar um tempo para tentar completar este desafio antes de verificar a solução. Praticar é a chave para um aprendizado eficaz.

Não fornecerei uma explicação completa de todas as etapas aqui, apenas algumas observações sobre os pontos importantes. Você pode encontrar o código da solução completa no repositório da disciplina no GitHub, tanto para Python quanto para C++.

Seu desafio é escrever um controlador para o nó `turtlesim`. Até agora, usamos apenas números básicos e simples para publicar e assinar tópicos. Com este exercício, você pode praticar como se estivesse trabalhando na lógica de um robô real.

### **O Desafio**

O objetivo é simples: queremos fazer a tartaruga se mover em círculos. Além disso, também queremos modificar a velocidade da tartaruga dependendo se ela está no lado direito ou esquerdo da tela.

Para obter a coordenada X de uma tartaruga na tela, você pode assinar o tópico `pose` daquela tartaruga. Então, encontrar o meio da tela é fácil: o valor X mínimo à esquerda é `0`, e o valor X máximo à direita é cerca de `11`. Assumiremos que a coordenada X para o meio da tela é `5.5`.

Você pode então enviar um comando de velocidade publicando no tópico `cmd_vel` da tartaruga. Para fazer a tartaruga se mover em um círculo, você só precisa publicar valores constantes para a velocidade linear (em X) e para a velocidade angular (em Z). Use `1.0` para ambas as velocidades se a tartaruga estiver à esquerda ($X < 5.5$), e `2.0` para ambas se a tartaruga estiver à direita.

Siga estas etapas para começar:

1. Crie um novo pacote (vamos chamá-lo de `turtle_controller`). Você pode decidir criar um pacote Python ou C++. Se fizer ambos, certifique-se de dar a cada um um nome diferente.
2. Dentro deste pacote, crie um novo nó chamado `turtle_controller`.
3. No construtor do nó, adicione um publicador (para a velocidade de comando) e um assinante (para a pose).
4. Aqui é onde as coisas ficam um pouco diferentes de antes: em vez de criar um temporizador (*timer*) e publicar a partir do *callback* do temporizador, **você pode publicar diretamente a partir do *callback* do assinante**. O nó `turtlesim` está constantemente publicando no tópico `pose`. Publicar um comando a partir do *callback* do assinante permite que você crie uma espécie de controle em malha fechada (*closed-loop control*). Você obtém a coordenada X atual e envia um comando de velocidade diferente, dependendo de onde a tartaruga está.
5. Para testar seu código, crie um executável. Em seguida, execute o `turtlesim` em um Terminal e o seu nó em outro. Você deverá ver a tartaruga desenhando um círculo, com uma velocidade diferente dependendo de que lado da tela ela está.

> **Observação**
>
> O Passo 4 descreve a essência de um **Sistema de Controle em Malha Fechada**. A publicação constante do `turtlesim` no tópico `pose` age como o nosso sensor (realimentação). O nosso *callback* de assinatura atua como o **Controlador**, avaliando a posição atual ($X$) e calculando imediatamente a ação de controle (a nova velocidade em `cmd_vel`). Como não estamos usando um temporizador para ditar o ritmo, a frequência de amostragem do nosso controle é perfeitamente ditada pela frequência com que o sensor consegue nos enviar dados!"

---
---
> **Atenção:**
>
>Pelo bem de seu aprendizado, tente realizar as etapas acima sem ler as informações adiante
---
---

## Solução para o Desafio de Tópicos – controle em malha fechada
Os passos para a solução são os seguintes
1. Criar um workspace
2. Criar um pacote (Python ou C++)
3. Criar um nó (Python ou C++)
4. Compilar (Python ou C++)
5. Executar os nós (Python ou C++)



### Criar um workspace
Vou conderar que você já criou um workspace no diretório `~/master_ros2_ws`conforme descrito na seçção [**Criando e configurando um workspace do ROS 2**](https://github.com/fabiobento/cont-int-2026-1/blob/main/nodes-ros2/nodes-ros2.md#criando-e-configurando-um-workspace-do-ros-2) da [**Aula 2: Escrevendo e Construindo um Nó ROS 2**](https://github.com/fabiobento/cont-int-2026-1/blob/main/nodes-ros2/nodes-ros2.md).

Vamos criar a solução em Python e em C++.

Começaremos com Python.

### Criar um pacote em Python
Você criará seus pacotes dentro do diretório do `src` do seu workspace, ou seja em `~/master_ros2_ws/src`. Então digite a seguinte linha de comando:
```bash
cd ~/master_ros2_ws/src
```
Você pode criar o pacote em Python ou em C++. Para criar o pacote em Python, digite a seguinte linha de comando:

```bash
ros2 pkg create turtle_controller --build-type ament_python --dependencies rclpy
```
### Criar um nó em Python
Para criar o nó, você deve criar um script Python dentro do diretório `~/master_ros2_ws/src/turtle_controller/turtle_controller`.
```bash
cd ~/master_ros2_ws/src/turtle_controller/turtle_controller
touch turtle_controller.py
```
Cole o seguinte código fonte no arquivo `turtle_controller.py`:
```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose


class TurtleControllerNode(Node):
    """
    Nó controlador para a tartaruga no ambiente turtlesim.
    Publica no tópico de velocidade e recebe informações do tópico de posição (pose).
    """

    def __init__(self):
        """
        Inicializa o nó ROS 2 com o nome 'turtle_controller'.
        Cria o publicador para '/turtle1/cmd_vel' e o assinante (subscriber) para '/turtle1/pose'.
        """
        super().__init__("turtle_controller")
        self.cmd_vel_pub_ = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.pose_sub_ = self.create_subscription(Pose, "/turtle1/pose", self.callback_pose, 10)

    def callback_pose(self, pose: Pose):
        """
        Função de callback chamada sempre que uma nova pose da tartaruga é recebida.
        Define e publica as velocidades linear e angular da tartaruga dependendo da sua coordenada 'x'.
        """
        cmd = Twist()
        if pose.x < 5.5:
            # Se a posição em x for menor que 5.5
            cmd.linear.x = 1.0
            cmd.angular.z = 1.0
        else:
            # Se a posição em x for maior ou igual a 5.5
            cmd.linear.x = 2.0
            cmd.angular.z = 2.0
        self.cmd_vel_pub_.publish(cmd)


def main(args=None):
    """
    Ponto de entrada principal do programa.
    Inicializa a comunicação ROS (rclpy), cria a instância do nó
    e o mantém em execução (spin) até que seja interrompido.
    """
    rclpy.init(args=args)
    node = TurtleControllerNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
```

Em seguida você edita a variável `entry_points` no arquivo `~/master_ros2_ws/src/turtle_controller/setup.py` para que ela fique assim:
```python
    entry_points={
        'console_scripts': [
            'turtle_controller = turtle_controller.turtle_controller:main',
        ],
    },
```
Isso adicionará o executável `turtle_controller` ao seu pacote.
O código fonte completo do `setup.py` fica assim *(também disponível [nesse link do repositório](https://github.com/fabiobento/cont-int-2026-1/blob/main/topics-ros2/scripts/turtle_controller/setup.py) )*:
```python
"""
Arquivo de configuração de instalação do pacote ROS 2 (Python).
Define as dependências, pontos de entrada (executáveis) e metadados do pacote.
"""
from setuptools import find_packages, setup

package_name = 'turtle_controller'

setup(
    name=package_name,
    version='0.0.0',
    # Busca automaticamente os pacotes e submódulos, excluindo pastas de testes
    packages=find_packages(exclude=['test']),
    data_files=[
        # Registra o pacote no índice de recursos do ament para ser localizado pelo ROS 2
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        # Instala o manifesto (package.xml) no diretório 'share' do pacote
        ('share/' + package_name, ['package.xml']),
    ],
    # Define os pacotes Python necessários para a instalação
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ed',
    maintainer_email='todo.todo@todo.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    # Define as dependências necessárias para rodar os testes
    tests_require=['pytest'],
    # Configuração dos executáveis do pacote (pontos de entrada)
    entry_points={
        'console_scripts': [
            # Cria o comando 'turtle_controller' apontando para a função 'main' do nó criado
            "turtle_controller = turtle_controller.turtle_controller:main"
        ],
    },
)

```

Além dissoas dependências, lembre-se que você importou as bibliotecas `geometry_msgs` e `turtlesim` no script `turtle_controller.py` de seu nó da seguinte forma:

```python
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
```
Portanto o seu nó "depende" delas, e elas devem ser adicionadas logo após `<depend>rclpy</depend>` no arquivo `~/master_ros2_ws/src/turtle_controller/package.xml`, e o trecho deve ficar assim:
```xml
  <depend>rclpy</depend>
  <depend>geometry_msgs</depend>
  <depend>turtlesim</depend>
```
> **Observação**
>
> Essas dependências já poderiam ter sido adicionadas logo na criação do pacote com a seguinte linha de comando:
> ```bash
> ros2 pkg create turtle_controller --build-type ament_python --dependencies rclpy geometry_msgs turtlesim
> ```
> Note que as dependências **`geometry_msgs`** e **`turtlesim`** foram adicionadas com o parâmetro **`--dependencies`**.

O arquivo `package.xml` completo fica assim *(também disponível [nesse link do repositório](https://github.com/fabiobento/cont-int-2026-1/blob/main/topics-ros2/scripts/turtle_controller/package.xml) )*:
```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <!-- Nome do pacote -->
  <name>turtle_controller</name>
  <!-- Versão atual do pacote -->
  <version>0.0.0</version>
  <!-- Breve descrição sobre o que o pacote faz -->
  <description>TODO: Package description</description>
  <!-- Nome e email do mantenedor responsável pelo pacote -->
  <maintainer email="todo.todo@todo.com">ed</maintainer>
  <!-- Declaração da licença de uso do código (ex: MIT, Apache-2.0) -->
  <license>TODO: License declaration</license>

  <!-- Dependências principais necessárias para a execução do pacote -->
  <depend>rclpy</depend>
  <depend>geometry_msgs</depend>
  <depend>turtlesim</depend>

  <!-- Dependências usadas exclusivamente para validação e testes (linters) -->
  <test_depend>ament_copyright</test_depend>
  <test_depend>ament_flake8</test_depend>
  <test_depend>ament_pep257</test_depend>
  <test_depend>python3-pytest</test_depend>

  <!-- Exportações adicionais para o sistema de build do ROS 2 -->
  <export>
    <!-- Define que este pacote deve ser compilado como um pacote Python -->
    <build_type>ament_python</build_type>
  </export>
</package>

```

### Compilar
Compile aplicação a partir do diretório raiz do workspace:
```bash
cd ~/master_ros2_ws
colcon build --symlink-install
```

### Executar os nós
Agora você pode executar os nós de sua aplicação em terminais separados. 
Primeiro execute o nó do ambiente virtual:
```bash
ros2 run turtlesim turtlesim_node
```
Você verá a janela do ambiente virtual com o robô (tartaruga) na posição inicial


![](https://github.com/fabiobento/cont-int-2026-1/blob/main/topics-ros2/imagens/turtlesim-node.png)


Em seguida execute o nó controlador:
```bash
ros2 run turtle_controller turtle_controller
```

Agora o robô estará seguindo a trajetória conforme a lógica implementada no nó controlador.

![](https://github.com/fabiobento/cont-int-2026-1/blob/main/topics-ros2/imagens/turtlesim-node-move.png)


Observe através do comando `rqt_graph` a relação entre os nós:
```bash
rqt_graph
```
> **Observação**
>
> Após executar o `rqt_graph` você possivelmente precisará clicar em `
Refresh ROS Graph` para que o gráfico seja atualizado.

Agora você tem um sistema em malha fechada, onde o nó controlador (`turtle_controller`) recebe informações do nó    (topico **`/turtle1/pose`**) do ambiente virtual (`turtlesim_node`) e publica comandos de velocidade para o mesmo (topico **`/turtle1/cmd_vel`**). 


![](https://github.com/fabiobento/cont-int-2026-1/blob/main/topics-ros2/imagens/rqtgraph-closed-loop.png)


O tópico `/turtle1/pose` publica mensagens do tipo `turtlesim/msg/Pose`. Confira isso ao digitar a segunte linha de comando:
```bash
ros2 topic info /turtle1/pose
```
A saída será:
```bash
Type: turtlesim/msg/Pose
Publisher count: 1
Subscription count: 1
```

Para inspecionar como é a interface da mensagem, digite a seguinte linha de comando:
```bash
ros2 interface show turtlesim/msg/Pose
```
A saída será:
```bash
msg
  float64 x
  float64 y
  float64 theta
  float64 linear_velocity
  float64 angular_velocity
```
Onde cada campo representa:
- **x**: Posição no eixo x
- **y**: Posição no eixo y
- **theta**: Orientação (ângulo) atual da tartaruga
- **linear_velocity**: Velocidade linear atual
- **angular_velocity**: Velocidade angular atual


O tópico `/turtle1/cmd_vel`, por sua vez, publica mensagens do tipo `geometry_msgs/msg/Twist`. Confira isso ao digitar a segunte linha de comando:
```bash
ros2 topic info /turtle1/cmd_vel
```
A saída será:
```bash
Type: geometry_msgs/msg/Twist
Publisher count: 1
Subscription count: 1
```

Para inspecionar como é a interface da mensagem, digite a seguinte linha de comando:
```bash
ros2 interface show geometry_msgs/msg/Twist
```
A saída será:
```bash
msg
  geometry_msgs/msg/Vector3 linear
    float64 x
    float64 y
    float64 z
  geometry_msgs/msg/Vector3 angular
    float64 x
    float64 y
    float64 z
```
Onde cada campo representa:
- **linear**: Componentes de velocidade linear (translação)
- **angular**: Componentes de velocidade angular (rotação)


### Criar um pacote em C++
Você cria o pacote em C++ da mesma forma que criou o pacote em Python, apenas mudando o argumento **`--build-type`** para **`ament_cmake`** e adicionando a dependência **`rclcpp`**.

```bash
cd ~/master_ros2_ws/src
ros2 pkg create turtle_controller_cpp --build-type ament_cmake --dependencies rclcpp geometry_msgs turtlesim
```
Note que, na linha acima, as dependências **`geometry_msgs`** e **`turtlesim`** foram adicionadas com o parâmetro **`--dependencies`**. Com isso, elas já foram adicionadas ao arquivo **`package.xml`** do pacote.

Com isso o arquivo `package.xml` do pacote `turtle_controller_cpp` já estará com as dependências necessárias com as diretivas `<depend>geometry_msgs</depend>` e `<depend>turtlesim</depend>`. Confira abaixo *(também disponível [nesse link do repositório](https://github.com/fabiobento/cont-int-2026-1/blob/main/topics-ros2/scripts/turtle_controller_cpp/package.xml) )*:
```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<!-- Define a versão do formato do manifesto do pacote ROS 2 (formato 3 é o padrão para ROS 2) -->
<package format="3">
  <!-- Nome do pacote, usado como identificador em todo o ecossistema ROS -->
  <name>turtle_controller_cpp</name>
  
  <!-- Versão atual do pacote -->
  <version>0.0.0</version>
  
  <!-- Breve descrição do objetivo deste pacote -->
  <description>TODO: Package description</description>
  
  <!-- Informações de contato do mantenedor (responsável pelo pacote) -->
  <maintainer email="todo.todo@todo.com">ed</maintainer>
  
  <!-- Tipo de licença sob a qual o pacote é distribuído -->
  <license>TODO: License declaration</license>

  <!-- Dependência da ferramenta de construção do ROS 2, necessária para compilar o código em C++ -->
  <buildtool_depend>ament_cmake</buildtool_depend>

  <!-- Dependências necessárias tanto para a fase de compilação quanto para a execução -->
  <!-- rclcpp: A biblioteca cliente padrão da linguagem C++ para ROS 2 -->
  <depend>rclcpp</depend>
  <!-- geometry_msgs: Fornece mensagens para dados geométricos (ex: Twist para velocidade linear/angular) -->
  <depend>geometry_msgs</depend>
  <!-- turtlesim: Pacote do simulador da tartaruga para acesso a interfaces como a de Pose -->
  <depend>turtlesim</depend>

  <!-- Dependências utilizadas apenas durante a fase de testes (são focadas em qualidade de código/linting) -->
  <test_depend>ament_lint_auto</test_depend>
  <test_depend>ament_lint_common</test_depend>

  <!-- Especifica comportamentos de exportação para outras ferramentas ROS 2 -->
  <export>
    <!-- Informa ao sistema que este pacote usa o ament_cmake como sistema de construção -->
    <build_type>ament_cmake</build_type>
  </export>
</package>

```

### Criar um nó em C++
Para criar o nó em C++ você deve criar um arquivo na pasta `~/master_ros2_ws/src/turtle_controller_cpp/turtle_controller_cpp/` com o nome `turtle_controller_cpp.cpp`
```bash
cd ~/master_ros2_ws/src/turtle_controller_cpp/src/
touch turtle_controller.cpp
```

Em seguida, cole o código abaixo *(também disponível [nesse link do repositório](https://github.com/fabiobento/cont-int-2026-1/blob/main/topics-ros2/scripts/turtle_controller_cpp/src/turtle_controller.cpp) )*:
```cpp
#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "turtlesim/msg/pose.hpp"

// Usado para facilitar a vinculação do parâmetro no callback
using namespace std::placeholders;

// Classe que define o nó ROS 2 para controlar a tartaruga
class TurtleControllerNode : public rclcpp::Node
{
public:
    // Construtor do nó, define o nome do nó como "turtle_controller"
    // Nota: usando rclcpp::Node para evitar o erro de namespace ocorrido anteriormente
    TurtleControllerNode() : rclcpp::Node("turtle_controller")
    {
        // Cria um publicador (publisher) no tópico "/turtle1/cmd_vel" para enviar comandos de velocidade
        cmd_vel_pub_ = this->create_publisher<geometry_msgs::msg::Twist>(
            "/turtle1/cmd_vel", 10);
            
        // Cria um assinante (subscriber) no tópico "/turtle1/pose" para receber a posição atual da tartaruga
        pose_sub_ = this->create_subscription<turtlesim::msg::Pose>(
            "/turtle1/pose", 10, std::bind(&TurtleControllerNode::poseCallback, this, _1));
    }

    // Função de callback acionada sempre que uma nova mensagem de posição é recebida
    void poseCallback(const turtlesim::msg::Pose::SharedPtr pose)
    {
        auto cmd = geometry_msgs::msg::Twist();
        
        // Verifica se a tartaruga está na metade esquerda (x < 5.5) ou direita (x >= 5.5) da tela
        if (pose->x < 5.5) {
            // Se estiver na parte esquerda, move-se mais devagar
            cmd.linear.x = 1.0;
            cmd.angular.z = 1.0;
        }
        else {
            // Se estiver na parte direita, move-se mais rápido
            cmd.linear.x = 2.0;
            cmd.angular.z = 2.0;
        }
        
        // Publica a mensagem de comando de velocidade
        cmd_vel_pub_->publish(cmd);
    }

private:
    // Ponteiros compartilhados para o publicador de velocidade e o assinante de posição
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr cmd_vel_pub_;
    rclcpp::Subscription<turtlesim::msg::Pose>::SharedPtr pose_sub_;
};

int main(int argc, char **argv)
{
    // Inicializa a infraestrutura de comunicação do ROS 2
    rclcpp::init(argc, argv);
    
    // Cria uma alocação de memória inteligente (smart pointer) para a instância do nó
    auto node = std::make_shared<TurtleControllerNode>();
    
    // Mantém o nó em execução contínua, processando os callbacks de eventos
    rclcpp::spin(node);
    
    // Finaliza adequadamente a execução do ROS 2 antes de encerrar o programa
    rclcpp::shutdown();
    return 0;
}
```

Conforme você estudou na seção [**Compilando e executando o nó**](https://github.com/fabiobento/cont-int-2026-1/blob/main/nodes-ros2/nodes-ros2.md#compilando-e-executando-o-n%C3%B3) da aula sobre nós ([Aula 2: Escrevendo e Construindo um Nó ROS 2](https://github.com/fabiobento/cont-int-2026-1/blob/main/nodes-ros2/nodes-ros2.md)), não podemos simplesmente executar o arquivo C++. Primeiro precisamos editar o arquivo `CMakeLists.txt` e adicionar o seguinte:
1. **Adicionar um novo executável** com a função `add_executable()`. Aqui, você deve escolher um nome para o executável (aquele que será usado com `ros2 run <nome_do_pacote> <nome_do_executavel>`) e também especificar o caminho relativo para o arquivo C++.
2. **Vincular todas as dependências** para este executável com a função `ament_target_dependencies()`.
3. **Instalar o executável** com a instrução `install()`, para que possamos encontrá-lo ao usar o `ros2 run`. Aqui, colocamos o executável em um diretório `lib/<nome_do_pacote>`.

Com isso esse trecho do arquivo `CMakeLists.txt` ficará assim:
```cmake
add_executable(turtle_controller src/turtle_controller.cpp)

ament_target_dependencies(turtle_controller rclcpp geometry_msgs turtlesim)

install(TARGETS
 turtle_controller
 DESTINATION lib/${PROJECT_NAME}/
)
```
O código e `CMakeLists.txt` é o seguinte *(também pode ser encontrado [nesse link do repositório](https://github.com/fabiobento/cont-int-2026-1/blob/main/topics-ros2/scripts/turtle_controller_cpp/CMakeLists.txt):
```cmake
# Define a versão mínima exigida do sistema de compilação CMake
cmake_minimum_required(VERSION 3.8)

# Define o nome do projeto (deve ser o mesmo nome contido no package.xml)
project(turtle_controller_cpp)

# Adiciona flags de compilação rigorosas caso o compilador seja GCC ou Clang.
# Isso ativa vários alertas (ex: variáveis não utilizadas) para melhorar a qualidade do código.
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Busca os pacotes do ROS 2 dos quais este projeto depende
# ament_cmake: Macros e funções principais de build do ROS 2
find_package(ament_cmake REQUIRED)
# rclcpp: Acesso às bibliotecas cliente C++ (como criar o nó, publishers, etc)
find_package(rclcpp REQUIRED)
# geometry_msgs: Acesso às classes de mensagens como o Twist
find_package(geometry_msgs REQUIRED)
# turtlesim: Acesso às interfaces específicas do simulador, como Pose
find_package(turtlesim REQUIRED)

# Declara a criação de um executável chamado "turtle_controller"
# Ele será compilado a partir do código-fonte localizado em "src/turtle_controller.cpp"
add_executable(turtle_controller src/turtle_controller.cpp)

# Vincula (link) as bibliotecas e diretórios de acesso (includes) dos pacotes ROS 2
# a este executável específico para que ele seja compilado corretamente
ament_target_dependencies(turtle_controller rclcpp geometry_msgs turtlesim)

# Instala o executável recém-criado na pasta de binários específicos de projeto
# Esta regra é o que permite o uso do comando `ros2 run turtle_controller_cpp turtle_controller`
install(TARGETS
 turtle_controller
 DESTINATION lib/${PROJECT_NAME}/
)

# Esta função finaliza as configurações do pacote, e cria ganchos (hooks) necessários
# para a correta instalação e exportação das bibliotecas/executáveis para outros pacotes
ament_package()
```

Agora é só compilar e executar os nós em C++

### Compilar os nós em C++
Compile aplicação a partir do diretório raiz do workspace:
```bash
cd ~/master_ros2_ws
colcon build --packages-select turtle_controller_cpp --symlink-install
```

### Executar os nós em C++
Agora você pode executar os nós de sua aplicação em terminais separados. 
Primeiro execute o nó do ambiente virtual(se ele já não estiver sendo executado):
```bash
ros2 run turtlesim turtlesim_node
```
Você verá a janela do ambiente virtual com o robô (tartaruga) na posição inicial


![](https://github.com/fabiobento/cont-int-2026-1/blob/main/topics-ros2/imagens/turtlesim-node.png)


Em seguida execute o nó controlador:
```bash
ros2 run turtle_controller_cpp turtle_controller
```

Agora o robô estará seguindo a trajetória conforme a lógica implementada no nó controlador.

![](https://github.com/fabiobento/cont-int-2026-1/blob/main/topics-ros2/imagens/turtlesim-node-move.png)


Observe através do comando `rqt_graph` a relação entre os nós:
```bash
rqt_graph
```
> **Observação**
>
> Após executar o `rqt_graph` você possivelmente precisará clicar em `
Refresh ROS Graph` para que o gráfico seja atualizado.

Observe que com o nó em C++ você tem um resultado igual ao do nó em Python: um sistema em malha fechada, onde o nó controlador (`turtle_controller`) recebe informações do nó    (topico **`/turtle1/pose`**) do ambiente virtual (`turtlesim_node`) e publica comandos de velocidade para o mesmo (topico **`/turtle1/cmd_vel`**). 


![](https://github.com/fabiobento/cont-int-2026-1/blob/main/topics-ros2/imagens/rqtgraph-closed-loop.png)