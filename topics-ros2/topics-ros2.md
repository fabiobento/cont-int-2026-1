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

Agora, abra este arquivo, utilize o template de nó orientado a objetos (disponibilizado na Aula 2) e modifique os campos necessários para usar nomes que façam sentido:

```python

```

