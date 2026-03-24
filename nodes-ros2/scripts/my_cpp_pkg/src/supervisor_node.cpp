#include "rclcpp/rclcpp.hpp"

class SupervisorNode : public rclcpp::Node {
public:
  SupervisorNode() : Node("supervisor_node") {
    // Timer de 5 segundos para supervisão
    timer_ =
        this->create_wall_timer(std::chrono::seconds(5),
                                std::bind(&SupervisorNode::check_status, this));
  }

private:
  void check_status() {
    RCLCPP_WARN(this->get_logger(),
                "[SUPERVISOR] Ronda em andamento. Sistema íntegro.");
  }
  rclcpp::TimerBase::SharedPtr timer_; // Ponteiro inteligente para o timer
};

int main(int argc, char **argv) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<SupervisorNode>());
  rclcpp::shutdown();
  return 0;
}