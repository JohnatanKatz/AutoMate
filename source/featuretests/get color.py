import win32gui
from pynput.mouse import Listener as Mouse_Listener
from pynput.keyboard import Listener as Key_Listener, Key

class ColorPicker:
    def get_pixel_color(self, x, y):
        """Get the color of the pixel at the given (x, y) screen coordinates."""
        hdc = win32gui.GetDC(None)
        color = win32gui.GetPixel(hdc, x, y)
        win32gui.ReleaseDC(None, hdc)
        # Convert color from int to RGB tuple
        blue = color & 0xff
        green = (color >> 8) & 0xff
        red = (color >> 16) & 0xff
        return red, green, blue

    def rgb_to_hex(self, rgb):
        """Convert an RGB tuple to a hex string."""
        return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])

    def on_click(self, x, y, button, pressed):
        if pressed:
            color = self.get_pixel_color(x, y)
            hex_color = self.rgb_to_hex(color)
            print(f"Clicked at ({x}, {y}), RGB Color: {color}, Hex Color: {hex_color}")

    def on_key_press(self, key):
        if key == Key.esc:
            return False  # Stop listener

    def start(self):
        with Key_Listener(on_press=self.on_key_press) as keyboard_listener, \
                Mouse_Listener(on_click=self.on_click) as mouse_listener:
            print("Color Picker active... Press 'Esc' to stop.")
            keyboard_listener.join()
            mouse_listener.stop()

# Using the class
color_picker = ColorPicker()
color_picker.start()
