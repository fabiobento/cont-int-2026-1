#include "rclcpp/rclcpp.hpp"

class MyCustomNode : public rclcpp::Node // MODIFIQUE O NOME
{
public:
  MyCustomNode()
      : Node("node_name") // MODIFIQUE O NOME
  {}

private:
};

int main(int argc, char **argv) {
  rclcpp::init(argc, argv);
  auto node = std::make_shared<MyCustomNode>(); // MODIFIQUE O NOME
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
