from contextlib import nullcontext
from std_msgs.msg import String
from rclpy.node import Node
from pynput import keyboard
import rclpy

class KeyboardRead(Node):

    def __init__(self):
        super().__init__('keyboard_read')
        self.publisher_ = self.create_publisher(String, 'directions', 10)


def on_press(key, node):    
    msg = String()
    msg.data = dict.get(key, 'STOP')
    node.publisher_.publish(msg)
    

dict = {
    keyboard.KeyCode(char = '8') : 'FWD',
    keyboard.KeyCode(char = '2') : 'BKWD',
    keyboard.KeyCode(char = '4') : 'L',
    keyboard.KeyCode(char = '6') : 'R',
    keyboard.KeyCode(char = '7') : 'FWD_L',
    keyboard.KeyCode(char = '9') : 'FWD_R',
    keyboard.KeyCode(char = '1') : 'BKWD_L',
    keyboard.KeyCode(char = '3') : 'BKWD_R',
    keyboard.KeyCode(char = 'x') : 'CW',
    keyboard.KeyCode(char = 'z') : 'CCW',
    keyboard.Key.space : 'STOP',
    keyboard.Key.esc : 'EXIT'  
}


def main(args=None):

    rclpy.init(args=args)
    keyboard_read = KeyboardRead()

    msg = String()
    msg.data = 'STOP'
    keyboard_read.publisher_.publish(msg)

    listener = keyboard.Listener(
        on_press=lambda event: on_press(event, keyboard_read)) 
    listener.start()

    keyboard_read.get_logger().info('Teleop ready')
    rclpy.spin(keyboard_read)

    keyboard_read.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
