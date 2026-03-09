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

**Um publicador (*publisher*) e um assinante (*subscriber*)**

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


![](https://github.com/fabiobento/cont-int-2026-1/raw/main/topics-ros2/imagens/radio-pub-sub-mult.jpg)
**Tópico com vários assinantes** ([Fonte](https://www.packtpub.com/en-us/product/ros-2-from-scratch-9781835881415))


![](https://github.com/fabiobento/cont-int-2026-1/raw/main/topics-ros2/imagens/radio-pub-mult-sub-mult.jpg)
**Tópico com vários publicadores e vários assinantes** ([Fonte](https://www.packtpub.com/en-us/product/ros-2-from-scratch-9781835881415))