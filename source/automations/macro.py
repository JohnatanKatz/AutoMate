import json
from pynput import keyboard, mouse
import time
#import ctypes

class Macro:
    def __init__(self):
        self.events = []

    def set_events(self, events):
        self.events = events

    def on_key_press(self, key):
        """try:
            print('alphanumeric key {0} pressed'.format(
                key.char))
        except AttributeError:
            print('special key {0} pressed'.format(
                key))"""
        if key == keyboard.Key.esc:
            return False  # Stop recording
        self.events.append(('key', 'press', key))

    def on_key_release(self, key):
        """print('{0} released'.format(
            key))"""
        self.events.append(('key', 'release', key))

    def on_click(self, x, y, button, pressed):
        """print('{0} at {1}'.format(
            'Pressed' if pressed else 'Released',
            (x, y)))"""
        self.events.append(('mouse', 'click', (x, y, button, pressed)))

    def on_scroll(self, x, y, dx, dy):
        self.events.append(('mouse', 'scroll', (x, y, dx, dy)))

    def on_esc_release(self, key):
        if key == keyboard.Key.esc:
            self.stop_recording = True  # Stop recording

    def record(self):
        with keyboard.Listener(on_press=self.on_key_press, on_release=self.on_key_release) as keyboard_listener, \
             mouse.Listener(on_click=self.on_click, on_scroll=self.on_scroll) as mouse_listener:

            print("Recording macro... Press 'Esc' to stop.")

            keyboard_listener.join()
            mouse_listener.stop()

    def return_dictionary(self):
        return {'type': 'macro', 'events': self.events}

    def load(self, file_name):
        with open(file_name, "r") as f:
            self.events = json.load(f)

    def play(self):
        keyboard_controller = keyboard.Controller()
        mouse_controller = mouse.Controller()

        for event in self.events:
            self.perform_action(event, keyboard_controller, mouse_controller)
            time.sleep(0.01)  # Delay might need some adjustment

    def perform_action(self, action, keyboard_controller, mouse_controller):
        event_type, action_type, data = action
        print(action)
        if event_type == 'key':
            key = data
            if action_type == 'press':
                keyboard_controller.press(key)
            elif action_type == 'release':
                keyboard_controller.release(key)
        elif event_type == 'mouse':
            if action_type == 'click':
                x, y, button, pressed = data
                print(x, y, button, pressed)
                if pressed == True:
                    mouse_controller.position = (x, y)
                    mouse_controller.click(button)
                else:
                    mouse_controller.position = (x, y)
                    mouse_controller.release(button)
            elif action_type == 'scroll':
                x, y, dx, dy = data
                mouse_controller.position = (x, y)
                mouse_controller.scroll(dx, dy)

def create_via_dictionary(dictionary):
    obj=Macro()
    obj.set_events(dictionary['events'])
    return obj



#PROCESS_PER_MONITOR_DPI_AWARE = 2

#ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)
#macro = Macro()
#macro.record()
#print(macro.events)
#macro.save("macro.json")
#macro.play()

"""
mouse_contoller = mouse.Controller()
mouse_contoller.position = (872, 63)
mouse_contoller.click(mouse.Button.left)
mouse_contoller.release(mouse.Button.left)
"""
"""
if __name__ == "__main__":
    macro = Macro()

    try:
        macro.record()
        macro.save("macro.json")

        new_macro = Macro()
        new_macro.load("macro.json")
        new_macro.play()
    except Exception as e:
        print("An error occurred:", e)
"""

"""
from typing import Any
from pynput._util import AbstractListener
from collections.abc import Callable

class KeyboardListener(AbstractListener):
    def __init__(
            self,
            on_press: Callable[[keyboard.Key | keyboard.KeyCode | None, mouse.Listener], None] | None = ...,
            on_release: Callable[[keyboard.Key | keyboard.KeyCode | None], None] | None = ...,
            suppress: bool = ...,
            **kwargs: Any,
    ) -> None: ...

    def canonical(self, key: keyboard.Key | keyboard.KeyCode) -> keyboard.Key | keyboard.KeyCode: ...
"""