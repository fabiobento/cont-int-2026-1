#include "geometry_msgs/msg/twist.hpp"
#include "rclcpp/rclcpp.hpp"
#include "turtlesim/msg/pose.hpp"

// Usado para facilitar a vinculação do parâmetro no callback
using namespace std::placeholders;

// Classe que define o nó ROS 2 para controlar a tartaruga
class TurtleControllerNode : public rclcpp::Node {
public:
  // Construtor do nó, define o nome do nó como "turtle_controller"
  // Nota: usando rclcpp::Node para evitar o erro de namespace ocorrido
  // anteriormente
  TurtleControllerNode() : rclcpp::Node("turtle_controller") {
    // Cria um publicador (publisher) no tópico "/turtle1/cmd_vel" para enviar
    // comandos de velocidade
    cmd_vel_pub_ = this->create_publisher<geometry_msgs::msg::Twist>(
        "/turtle1/cmd_vel", 10);

    // Cria um assinante (subscriber) no tópico "/turtle1/pose" para receber a
    // posição atual da tartaruga
    pose_sub_ = this->create_subscription<turtlesim::msg::Pose>(
        "/turtle1/pose", 10,
        std::bind(&TurtleControllerNode::poseCallback, this, _1));
  }

  // Função de callback acionada sempre que uma nova mensagem de posição é
  // recebida
  void poseCallback(const turtlesim::msg::Pose::SharedPtr pose) {
    auto cmd = geometry_msgs::msg::Twist();

    // Verifica se a tartaruga está na metade esquerda (x < 5.5) ou direita (x
    // >= 5.5) da tela
    if (pose->x < 5.5) {
      // Se estiver na parte esquerda, move-se mais devagar
      cmd.linear.x = 1.0;
      cmd.angular.z = 1.0;
    } else {
      // Se estiver na parte direita, move-se mais rápido
      cmd.linear.x = 2.0;
      cmd.angular.z = 2.0;
    }

    // Publica a mensagem de comando de velocidade
    cmd_vel_pub_->publish(cmd);
  }

private:
  // Ponteiros compartilhados para o publicador de velocidade e o assinante de
  // posição
  rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr cmd_vel_pub_;
  rclcpp::Subscription<turtlesim::msg::Pose>::SharedPtr pose_sub_;
};

int main(int argc, char **argv) {
  // Inicializa a infraestrutura de comunicação do ROS 2
  rclcpp::init(argc, argv);

  // Cria uma alocação de memória inteligente (smart pointer) para a instância
  // do nó
  auto node = std::make_shared<TurtleControllerNode>();

  // Mantém o nó em execução contínua, processando os callbacks de eventos
  rclcpp::spin(node);

  // Finaliza adequadamente a execução do ROS 2 antes de encerrar o programa
  rclcpp::shutdown();
  return 0;
}