import pygetwindow as gw
from pynput.mouse import Listener as Mouse_Listener
from pynput.keyboard import Key, Listener as Key_Listener

class WindowDynamics:

    def __init__(self):
        self.window = ""
        self.toggle = "Focus"

    def set_window(self, window):
        self.window = window

    def set_toggle(self, toggle):
        self.toggle = toggle

    def unset_all(self):
        self.window = ""
        self.toggle = "Focus"

    def get_window_under_mouse(self):
        return gw.getActiveWindow()

    def play(self):
        print("Playing window dynamics", self.window, self.toggle)
        if self.window == "":
            raise Exception("Window title is empty")

        windows = gw.getWindowsWithTitle(self.window)
        if len(windows) == 0:
            print("No window found with title:", self.window)
            return
        print(windows)
        window = windows[0]
        print(window)
        if self.toggle == "Minimize":
            window.minimize()
        elif self.toggle == "Maximize":
            window.maximize()
        elif self.toggle == "Focus":
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

    def return_dictionary(self):
        return {'type': 'windowDynamics', 'window': self.window, 'toggle': self.toggle}

def create_via_dictionary(dictionary):
    obj=WindowDynamics()
    obj.set_window(dictionary['window'])
    obj.set_toggle(dictionary['toggle'])
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