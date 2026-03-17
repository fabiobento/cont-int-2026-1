#!/usr/bin/env python3
import rclpy
from rclpy.node import Node


class MyCustomNode(Node): # MODIFIQUE O NOME
    def __init__(self):
        super().__init__("node_name") # MODIFIQUE O NOME


def main(args=None):
    rclpy.init(args=args)
    node = MyCustomNode() # MODIFIQUE O NOME
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
