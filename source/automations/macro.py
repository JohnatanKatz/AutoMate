import json
from pynput import keyboard, mouse
import time
#import ctypes

class Macro:
    def __init__(self):
        self.events = []

    def set_events(self, events):
        self.events = events

    def unset_events(self):
        self.events = []

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

    """def return_dictionary(self):
        print (self.events)
        events_json_ready = [list(event) for event in self.events]
        print (events_json_ready)
        return {'type': 'macro', 'events': events_json_ready}"""

    def return_dictionary(self):
        events_json_ready = []
        for event in self.events:
            event_type, action_type, data = event
            if event_type == 'key':
                # Convert pynput key object to string
                if isinstance(data, keyboard.Key):
                    data = str(data)
                elif isinstance(data, keyboard.KeyCode):
                    data = data.char
            elif event_type == 'mouse':
                if action_type == 'click':
                    x, y, button, pressed = data
                    data = (x, y, str(button), pressed)
                elif action_type == 'scroll':
                    x, y, dx, dy = data
                    data = (x, y, dx, dy)

            events_json_ready.append((event_type, action_type, data))

        return {'type': 'macro', 'events': events_json_ready}

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

"""
def create_via_dictionary(dictionary):
    print(dictionary)
    obj=Macro()
    events=[tuple(event) for event in dictionary['events']]
    obj.set_events(events)
    return obj

def create_via_dictionary(dictionary):
    macro_obj = Macro()
    converted_events = []

    for event in dictionary['events']:
        event_type, action_type, data = event
        if event_type == 'key':
            # Convert the string representation back to a key object
            data = convert_string_to_key(data)
        elif event_type == 'mouse' and action_type == 'click':
            x, y, button, pressed = data
            button = convert_string_to_mouse_button(button)
            data = (x, y, button, pressed)
        # Append the reconstructed event to the list
        converted_events.append((event_type, action_type, data))

    macro_obj.set_events(converted_events)
    return macro_obj
"""

def create_via_dictionary(dictionary):
    print(dictionary)
    macro_obj = Macro()
    converted_events = []

    for event in dictionary['events']:
        event_type, action_type, data = event
        if event_type == 'key':
            # Convert the string representation back to a key object
            key_data = data
            if len(key_data) == 1:
                # It's a regular key
                converted_key = keyboard.KeyCode.from_char(key_data)
            else:
                # It's a special key like 'Key.f1', 'Key.esc', etc.
                key_name = key_data.split('.')[1]  # Get the part after 'Key.'
                converted_key = getattr(keyboard.Key, key_name, None)  # Use getattr to get the Key object
            converted_events.append((event_type, action_type, converted_key))
        elif event_type == 'mouse':
            if action_type == 'click':
                x, y, button, pressed = data
                button = getattr(mouse.Button, button.split('.')[1])  # Convert string to Button object
                data = (x, y, button, pressed)
            # Note: For mouse scroll, the data can be used as-is
            converted_events.append((event_type, action_type, data))

    macro_obj.set_events(converted_events)
    return macro_obj







"""
def convert_string_to_key(key_str):
    # Convert a string to a pynput key object
    try:
        return getattr(keyboard.Key, key_str)  # For special keys like 'esc', 'ctrl', etc.
    except AttributeError:
        return keyboard.KeyCode.from_char(key_str)  # For alphanumeric characters

def convert_string_to_mouse_button(button_str):
    # Convert a string to a pynput mouse button object
    return getattr(mouse.Button, button_str)

def parse_event(event_str):
    parts = event_str.split(' ')
    if parts[0] == 'mouse':
        # Parsing mouse event
        pos = tuple(map(int, parts[2][1:-1].split(',')))  # Remove parentheses and split
        return (parts[0], parts[1], pos, parts[3] == 'True')
    else:
        # Parsing key event
        return (parts[0], parts[1], parts[2])

"""
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