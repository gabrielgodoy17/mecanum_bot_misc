from contextlib import nullcontext
from std_msgs.msg import String
from rclpy.node import Node
from pynput import keyboard
import rclpy

class KeyboardRead(Node):

    def __init__(self):
        super().__init__('keyboard_read')
        self.publisher_ = self.create_publisher(String, 'directions', 10)
        timer_period = 0.005  # seconds

        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        global to_send_old
        global to_send_new

        #if to_send_old != to_send_new :
        msg = String()
        msg.data = to_send_new
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1
        to_send_old=to_send_new


def on_activate_FWD():
    global to_send_new
    to_send_new = "FWD"

def on_activate_BKWD():
    global to_send_new
    to_send_new = "BKWD" 

def on_activate_L():
    global to_send_new
    to_send_new = "L"

def on_activate_R():
    global to_send_new
    to_send_new = "R"   

def on_activate_FWD_L():
    global to_send_new
    to_send_new = "FWD_L"

def on_activate_FWD_R():
    global to_send_new
    to_send_new = "FWD_R"

def on_activate_BKWD_L():
    global to_send_new
    to_send_new = "BKWD_L"

def on_activate_BKWD_R():
    global to_send_new
    to_send_new = "BKWD_R"

def on_activate_CW():
    global to_send_new
    to_send_new = "CW"

def on_activate_CCW():
    global to_send_new
    to_send_new = "CCW"

def on_activate_STOP():
    global to_send_new
    to_send_new = "STOP"

def on_activate_EXIT():
    global to_send_new
    to_send_new = "EXIT"


def on_press(key):    
    func = dict.get(key, on_activate_STOP)
    func()

dict = {
    keyboard.KeyCode(char = '8') : on_activate_FWD,
    keyboard.KeyCode(char = '2') : on_activate_BKWD,
    keyboard.KeyCode(char = '4') : on_activate_L,
    keyboard.KeyCode(char = '6') : on_activate_R,
    keyboard.KeyCode(char = '7') : on_activate_FWD_L,
    keyboard.KeyCode(char = '9') : on_activate_FWD_R,
    keyboard.KeyCode(char = '1') : on_activate_BKWD_L,
    keyboard.KeyCode(char = '3') : on_activate_BKWD_R,
    keyboard.KeyCode(char = 'x') : on_activate_CW,
    keyboard.KeyCode(char = 'z') : on_activate_CCW,
    keyboard.Key.space : on_activate_STOP,
    keyboard.Key.esc : on_activate_EXIT  
}


def main(args=None):

    rclpy.init(args=args)
    keyboard_read = KeyboardRead()

    global to_send_old
    global to_send_new
    to_send_old = " "
    to_send_new = "STOP"

    listener = keyboard.Listener(
        on_press=on_press) 
    listener.start()

    rclpy.spin(keyboard_read)
    # with keyboard.GlobalHotKeys({
    # '8' : on_activate_FWD,
    # '2' : on_activate_BKWD,
    # '4' : on_activate_L,
    # '6' : on_activate_R,
    # '7' : on_activate_FWD_L,
    # '9' : on_activate_FWD_R,
    # '1' : on_activate_BKWD_L,
    # '3' : on_activate_BKWD_R,
    # 'x' : on_activate_CW,
    # 'z' : on_activate_CCW,
    # '<space>' : on_activate_STOP,
    # }) as h: h.join()

    
    # algo.press('A')
    # algo.release('A')
    
    # with algo.pressed('8') : on_activate_FWD


    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    keyboard_read.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
