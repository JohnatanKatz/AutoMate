import win32gui
import tkinter as tk
from tkinter import Canvas
from pynput.mouse import Listener as Mouse_Listener
from pynput.keyboard import Listener as Key_Listener, Key
import threading
import colorsys

class ColorPicker:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Picker")
        self.root.wm_attributes('-topmost', True)  # Set window to always stay on top
        self.is_listening = False
        self.stop_key = None

        self.last_color_rgb = (0, 0, 0)
        self.last_color_hex = "#000000"
        self.last_color_hsl = (0, 0, 0)

        # Create GUI elements
        self.start_button = tk.Button(root, text="Start", command=self.start_listening)
        self.stop_button = tk.Button(root, text="Stop", state="disabled", command=self.stop_listening)
        self.color_label = tk.Label(root, text="Last Color:")
        self.rgb_label = tk.Label(root, text="RGB Color:")
        self.hex_label = tk.Label(root, text="Hex Color:")
        self.hsl_label = tk.Label(root, text="HSL Color:")
        self.stop_key_label = tk.Label(root, text="Stop Key:")
        self.stop_key_entry = tk.Entry(root)
        self.stop_key_entry.insert(0, "Esc")  # Default stop key

        # Create a canvas to display the last clicked color
        self.color_display = Canvas(root, width=50, height=50, background=self.last_color_hex)

        # Place GUI elements in the window
        self.start_button.pack()
        self.stop_button.pack()
        self.color_label.pack()
        self.rgb_label.pack()
        self.hex_label.pack()
        self.hsl_label.pack()
        self.stop_key_label.pack()
        self.stop_key_entry.pack()
        self.color_display.pack()

    def get_pixel_color(self, x, y):
        hdc = win32gui.GetDC(None)
        color = win32gui.GetPixel(hdc, x, y)
        win32gui.ReleaseDC(None, hdc)
        blue = color & 0xff
        green = (color >> 8) & 0xff
        red = (color >> 16) & 0xff
        return red, green, blue

    def rgb_to_hex(self, rgb):
        return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])

    def rgb_to_hsl(self, rgb):
        r, g, b = [x / 255.0 for x in rgb]
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        return int(h * 360), int(s * 100), int(l * 100)

    def update_color_labels(self, color):
        self.last_color_rgb = color
        self.last_color_hex = self.rgb_to_hex(color)
        self.last_color_hsl = self.rgb_to_hsl(color)
        self.color_label.config(text=f"Last Color: RGB({color[0]}, {color[1]}, {color[2]})")
        self.rgb_label.config(text=f"RGB Color: ({color[0]}, {color[1]}, {color[2]})")
        self.hex_label.config(text=f"Hex Color: {self.last_color_hex}")
        self.hsl_label.config(text=f"HSL Color: ({self.last_color_hsl[0]}, {self.last_color_hsl[1]}%, {self.last_color_hsl[2]}%)")
        self.color_display.config(background=self.last_color_hex)

    def on_click(self, x, y, button, pressed):
        if pressed:
            color = self.get_pixel_color(x, y)
            self.update_color_labels(color)

    def start_listening(self):
        if not self.is_listening:
            self.stop_key = self.stop_key_entry.get()
            self.is_listening = True
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            self.update_color_labels(self.last_color_rgb)
            print(f"Color Picker active... Press '{self.stop_key}' to stop.")
            keyboard_listener = Key_Listener(on_press=self.on_key_press)
            mouse_listener = Mouse_Listener(on_click=self.on_click)
            keyboard_thread = threading.Thread(target=keyboard_listener.run)
            mouse_thread = threading.Thread(target=mouse_listener.run)
            keyboard_thread.start()
            mouse_thread.stop()

    def stop_listening(self):
        if self.is_listening:
            self.is_listening = False
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            print("Color Picker stopped.")

    def on_key_press(self, key):
        if key == getattr(Key, self.stop_key, None):
            self.stop_listening()

if __name__ == "__main__":
    root = tk.Tk()
    color_picker = ColorPicker(root)
    root.mainloop()
