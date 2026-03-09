# **Tópicos – Enviando e Recebendo Mensagens entre Nós**

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
$ cd ~/master_ros2_ws/src/my_py_pkg/my_py_pkg/
$ touch number_publisher.py
$ chmod +x number_publisher.py
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
$ ros2 interface show example_interfaces/msg/Int64
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

**Compilando o publicador**

Para testar seu código, você precisa instalar o nó.

Antes de fazermos isso, como estamos usando uma nova dependência (o pacote `example_interfaces`), também precisamos adicionar uma linha ao arquivo `package.xml` do pacote `my_py_pkg`:

```xml
<depend>rclpy</depend>
<depend>example_interfaces</depend>
```

À medida que você adicionar mais funcionalidades dentro do seu pacote, você adicionará qualquer outra dependência do ROS 2 aqui.

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

Agora, vá para o diretório raiz do seu workspace e compile o pacote `my_py_pkg`:

```bash
cd ~/master_ros2_ws/
colcon build --packages-select my_py_pkg --symlink-install
```
Usamos `--symlink-install` para que não precisemos rodar o `colcon build` toda vez que modificarmos o nó `number_publisher`.

**Executando o publicador**

Após o pacote ter sido compilado com sucesso, faça o *source* do seu *workspace* e inicie o nó:

```bash
source ~/master_ros2_ws/install/setup.bash
ros2 run my_py_pkg number_publisher
[INFO] [1773082036.235805556] [number_publisher]: O publicador de números foi iniciado
```

O nó está rodando, mas além do log inicial, nada é exibido. Isso é normal — não pedimos para o nó imprimir mais nada.

Como sabemos que o publicador está funcionando? Poderíamos escrever um nó assinante agora mesmo e ver se recebemos as mensagens. Mas, antes de fazermos isso, podemos testar o publicador diretamente do Terminal.

Abra uma nova janela de Terminal e liste todos os tópicos:

```bash
$ ros2 topic list
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
$ ros2 topic echo /number
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
$ cd ~/master_ros2_ws/src/my_cpp_pkg/src/
$ touch number_publisher.cpp
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

**Compilando e executando o publicador**

Uma vez que você tenha escrito o nó com o publicador, temporizador e função de *callback*, é hora de compilá-lo.

Como fizemos para o Python, abra o arquivo `package.xml` do pacote `my_cpp_pkg` e adicione uma linha para a dependência ao `example_interfaces`:

```xml
<depend>rclcpp</depend>
<depend>example_interfaces</depend>

```

Em seguida, abra o arquivo `CMakeLists.txt` do pacote `my_cpp_pkg` e adicione as seguintes linhas:

```cmake
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

```

Para qualquer nova dependência de mensagem, precisamos adicionar uma nova linha `find_package()`.

Em seguida, criamos um novo executável. Note que também fornecemos `example_interfaces` nos argumentos de `ament_target_dependencies()`. Se você omitir isso, o vinculador (linker) do C++ falhará e você receberá um erro durante a compilação.

Por fim, não há necessidade de recriar o bloco `install()`. Apenas adicione o nome do novo executável em uma nova linha dentro dele, **sem vírgulas** entre as linhas (diferente do Python).

Agora, você pode compilar, carregar as variáveis de ambiente (*source*) e executar:

```bash
cd ~/master_ros2_ws/
colcon build --packages-select my_cpp_pkg
source install/setup.bash
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
$ cd ~/master_ros2_ws/src/my_py_pkg/my_py_pkg/
$ touch number_counter.py
$ chmod +x number_counter.py

```

Neste arquivo, você pode escrever o código para o nó e adicionar um assinante. Aqui está a explicação, passo a passo:

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64
```

Como queremos criar um assinante para receber o que enviamos com o publicador, precisamos usar a mesma interface. Portanto, também importamos `Int64`. Em seguida, podemos criar o assinante:

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

**Observação**
Como boa prática, especifiquei o tipo `Int64` para o argumento `msg` do método. Isso não é obrigatório para que o código Python funcione, mas adiciona um nível extra de segurança (temos certeza de que devemos receber um `Int64` e nada mais) e, às vezes, pode fazer com que o preenchimento automático (*auto-completion*) da sua IDE funcione melhor.

Para finalizar o nó, não se esqueça de adicionar a função padrão `main()` após a classe `NumberCounterNode`.

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
Mesmo que as bibliotecas `rclpy` e `rclcpp` devam ser baseadas no mesmo código subjacente, ainda pode haver algumas diferenças na API. Não se preocupe se o código às vezes não parecer o mesmo entre Python e C++.

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

Em seguida, compile o pacote `my_cpp_pkg`, carregue o *workspace* e execute tanto o nó publicador quanto o nó assinante em Terminais diferentes. Você deve ver uma saída semelhante à que tivemos com o Python.

### **Executando os nós em Python e C++ juntos**

Acabamos de criar um publicador e um assinante tanto em Python quanto em C++. O tópico que utilizamos possui o mesmo nome (`number`) e a mesma interface (`example_interfaces/msg/Int64`).

Se o tópico é o mesmo, isso significa que você poderia iniciar o nó `number_publisher` em Python junto com o nó `number_counter` em C++, por exemplo.

Vamos verificar isso:

```bash
$ ros2 run my_py_pkg number_publisher
[INFO] [1711597703.615546913] [number_publisher]: Number publisher has been started.

$ ros2 run my_cpp_pkg number_counter
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

Se necessário, atualize a visualização algumas vezes e selecione `Nodes/Topics (all)`. Você também pode desmarcar a caixa `Dead sinks` e a caixa `Leaf topics`. Isso permitirá que você veja os tópicos mesmo se houver apenas um assinante e nenhum publicador, ou um publicador e nenhum assinante:


![](https://github.com/fabiobento/cont-int-2026-1/raw/main/topics-ros2/imagens/topics-rqt.png)
**O tópico `number` no rqt_graph** (Fonte: O autor, gerado via `rqt_graph`)

Lá, podemos ver o nó `number_publisher` e o nó `number_counter`. No meio, temos o tópico `/number`, e podemos ver qual nó é um publicador ou um assinante.

O pacote `rqt_graph` pode ser extremamente útil ao depurar tópicos. Imagine que você executa alguns nós e se pergunta por que as mensagens do tópico não são recebidas por um assinante. Talvez esses nós não estejam usando o mesmo nome de tópico. Você pode ver isso facilmente com o `rqt_graph`:

*[Figura 5.8 – Incompatibilidade de nome de tópico entre publicador e assinante]*

Neste exemplo, cometi um erro intencional no nome do tópico dentro do publicador. Em vez de `number`, escrevi `numberr`. Com o `rqt_graph`, posso ver onde está o problema. Os dois nós não estão se comunicando um com o outro.


### **A linha de comando ros2 topic**

Com o `ros2 node`, obtemos ferramentas de linha de comando adicionais para os nós. Para os tópicos, usaremos o `ros2 topic`.

Se você executar `ros2 topic -h`, verá que há muitos comandos. Você já conhece alguns deles. Aqui, farei uma rápida recapitulação e explorarei mais alguns comandos que podem ser úteis ao depurar tópicos.

Primeiro, para listar todos os tópicos, use `ros2 topic list`:

```bash
$ ros2 topic list
/number
/parameter_events
/rosout

```

Como você pode ver, obtemos o tópico `/number`. Você também sempre obterá `/parameter_events` e `/rosout` (todos os logs do ROS 2 são publicados neste tópico).

Com `ros2 topic info <nome_do_topico>`, você pode obter a interface do tópico, bem como o número de publicadores e assinantes para aquele tópico:

```bash
$ ros2 topic info /number
Type: example_interfaces/msg/Int64
Publisher count: 1
Subscription count: 1

```

Então, para ir mais longe e ver os detalhes da interface, você pode executar o seguinte comando:

```bash
$ ros2 interface show example_interfaces/msg/Int64
# some comments
int64 data

```

Com isso, temos todas as informações de que precisamos para criar um publicador ou assinante adicional para o tópico.

Além disso, também podemos assinar o tópico diretamente pelo Terminal com `ros2 topic echo <nome_do_topico>`. Foi o que fizemos logo após escrever o publicador para garantir que ele estivesse funcionando antes de escrevermos qualquer assinante:

```bash
$ ros2 topic echo /number
data: 2
---
data: 2
---

```

Por outro lado, você pode publicar em um tópico diretamente pelo Terminal com `ros2 topic pub -r <frequência> <nome_do_topico> <interface> <mensagem_em_json>`. Para testar isso, pare todos os nós e inicie apenas o nó `number_counter` em um Terminal. Além do log inicial, nada será impresso. Em seguida, execute o seguinte comando em outro Terminal:

```bash
$ ros2 topic pub -r 2.0 /number example_interfaces/msg/Int64 "{data: 7}"
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

---

### **Alterando o nome de um tópico em tempo de execução**

Na Aula 2, você aprendeu como alterar o nome de um nó em tempo de execução — ou seja, adicionando `--ros-args -r __node:=<novo_nome>` após o comando `ros2 run`.

Então, para qualquer argumento adicional que você passar após o `ros2 run`, adicione `--ros-args`, mas apenas uma vez.

Logo, você também pode alterar o nome de um tópico em tempo de execução. Para fazer isso, adicione outro `-r`, seguido por `<nome_do_topico>:=<novo_nome_do_topico>`.

Por exemplo, vamos renomear nosso tópico de `number` para `my_number`:

```bash
$ ros2 run my_py_pkg number_publisher --ros-args -r number:=my_number

```

Agora, se iniciarmos o nó `number_counter`, para podermos receber as mensagens, também precisamos modificar o nome do tópico dele:

```bash
$ ros2 run my_py_pkg number_counter --ros-args -r number:=my_number

```

Com isso, a comunicação funcionará, mas desta vez usando o tópico `my_number`.

Para tornar as coisas um pouco mais interessantes, vamos manter esses dois nós rodando e vamos executar outro publicador para este tópico, usando o mesmo nó `number_publisher`. Como você sabe, não podemos ter dois nós rodando com o mesmo nome. Portanto, teremos que renomear tanto o nó quanto o tópico. Em um terceiro Terminal, execute o seguinte comando:

```bash
$ ros2 run my_py_pkg number_publisher --ros-args -r __node:=number_publisher_2 -r number:=my_number

```

Após executar isso, você verá que o `number_counter` recebe mensagens duas vezes mais rápido, já que há dois nós publicando uma mensagem a cada `1.0` segundo.

Além disso, vamos iniciar o `rqt_graph`:

*[Figura 5.9 – Dois publicadores e um assinante, com um tópico renomeado]*

Veremos que temos dois nós contendo um publicador no tópico `my_number` e um nó contendo um assinante.

A alteração de nomes de tópicos em tempo de execução será bastante útil para você, especialmente quando quiser executar vários nós existentes que você não pode modificar (por exemplo, os nós dos drivers das câmeras no Raspberry Pi do nosso projeto). Mesmo que você não possa reescrever o código, você pode modificar os nomes na hora de rodar.

---

### **Reproduzindo dados de tópicos com bags**

Imagine este cenário: você está trabalhando em um robô móvel que deve ter um determinado desempenho ao navegar do lado de fora enquanto está chovendo.

Isso significa que você precisará executar o robô nessas condições para poder desenvolver sua aplicação. Há alguns problemas: talvez você não tenha acesso ao robô o tempo todo, ou não possa levá-lo para fora, ou simplesmente não chove todo dia.

Uma solução para isso é usar bags (*ROS 2 bags*). Os bags permitem que você grave um tópico e o reproduza mais tarde. Assim, você pode executar o experimento uma vez com as condições necessárias e, em seguida, reproduzir os dados exatamente como foram gravados. Com esses dados em loop, você pode desenvolver a sua aplicação de controle no conforto do laboratório.

Vamos considerar outro cenário comum em Sistemas Embarcados: você trabalha com um hardware (um sensor ultrassônico ou uma IMU) que ainda não está estável. Na maior parte do tempo, ele não funciona corretamente. Você poderia gravar um bag enquanto o hardware estiver funcionando bem e, em seguida, reproduzir esse bag para desenvolver sua aplicação de controle em vez de tentar usar o hardware de novo e de novo e perder tempo com as falhas dele.

Para trabalhar com bags no ROS 2, você deve usar a ferramenta de linha de comando `ros2 bag`. Vamos aprender como salvar e reproduzir um tópico com bags.

Primeiro, pare todos os nós e execute apenas o nó `number_publisher`.

Já sabemos que o nome do tópico é `/number`. Você pode recuperar isso com `ros2 topic list` se necessário. Em seguida, em outro Terminal, grave o bag com `ros2 bag record <lista_de_topicos> -o <nome_do_bag>`. Para deixar as coisas mais organizadas, sugiro que você crie uma pasta `bags` e grave de dentro dessa pasta:

```bash
$ mkdir ~/bags
$ cd ~/bags/
$ ros2 bag record /number -o bag1
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
$ ros2 bag play ~/bags/bag1/

```

Isso publicará todas as mensagens gravadas, com a mesma duração da gravação. Então, se você gravou por 3 minutos e 14 segundos, o bag reproduzirá o tópico por 3 minutos e 14 segundos. Depois disso, o bag será encerrado, e você poderá reproduzi-lo novamente se quiser.

Enquanto o bag estiver sendo reproduzido, você pode executar seu(s) assinante(s). Você pode fazer um teste rápido com `ros2 topic echo /number` e ver os dados passando. Você também pode executar seu nó `number_counter`, e verá que as mensagens são recebidas como se o sensor real estivesse lá.

Você agora é capaz de salvar e reproduzir um tópico usando os bags do ROS 2. Você pode explorar opções mais avançadas usando `ros2 bag -h`.

Como você viu, existem várias ferramentas disponíveis para lidar com tópicos. Use essas ferramentas com a maior frequência possível para inspecionar, depurar e testar seus tópicos. Elas pouparão muito do seu tempo ao desenvolver sua aplicação de controle no ROS 2.

Estamos quase terminando com os tópicos. Até agora, tudo o que fizemos foi usar interfaces (*messages*) existentes. A seguir, vamos aprender como criar uma interface de dados personalizada.

> **Observação**
>
> É exatamente assim que se trabalha com *Machine Learning* e *MLOps* aplicado à robótica. O fluxo de trabalho padrão da indústria é colocar o robô em operação, usar o `ros2 bag record` para gravar os dados dos sensores (câmera, lidar, posição), e depois usar esse `.mcap` gravado para treinar as redes neurais e algoritmos genéticos *offline*, garantindo que os dados de treino reflitam as condições reais do hardware.
