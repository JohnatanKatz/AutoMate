import pygetwindow as gw
from pynput.mouse import Listener as Mouse_Listener
from pynput.keyboard import Key, Listener as Key_Listener

class WindowDynamics:

    def __init__(self):
        self.window = ""

    def set_window(self, window):
        self.window = window

    def get_window_under_mouse(self):
        return gw.getActiveWindow()

    def toggle_window(self, toggle):
        if self.window == "":
            raise Exception("")
        window = gw.getWindowsWithTitle(self.window)
        if toggle == "minimize":
            window.minimize()
        elif toggle == "maximize":
            window.maximize()
        elif toggle == "focus":
            window.activate()

    def on_click(self, x, y, button, pressed):
        if pressed:
            window = self.get_window_under_mouse()
            self.window = window.title

    def on_key_press(self, key):
        if key == Key.esc:
            return False  # Stop window

    def record(self):
        with Key_Listener(on_press=self.on_key_press) as keyboard_listener, \
                Mouse_Listener(on_click=self.on_click) as mouse_listener:
            print("Recording window... Press 'Esc' to stop.")
    
            keyboard_listener.join()
            mouse_listener.stop()

def create_via_dictionary(dictionary):
    obj=WindowDynamics()
    obj.set_window(dictionary['window'])
    return obj


"""
def get_window_under_mouse():
    return gw.getActiveWindow()

def save_window_info(window_title):
    with open("window_info.txt", "a", encoding="utf-8") as file:
        file.write(f"{datetime.now()}: {window_title}\n")

def on_click(x, y, button, pressed):
    if pressed:
        window = get_window_under_mouse()
        window_title = window.title
        save_window_info(window_title)
        print(f"Clicked on: {window_title}")

# Create a listener thread for mouse events
with Listener(on_click=on_click) as listener:
    listener.join()


"""