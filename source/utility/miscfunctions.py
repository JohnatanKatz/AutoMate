import base64
import subprocess  # for calling a program
from PIL import ImageGrab, Image  # for handling the clipboard and images
from io import BytesIO
import platform

def get_cut_image():
    """

    :return:
    """
    # need to add Apple support
    #subprocess.call([r'C:\\Windows\System32\SnippingTool.exe', '/clip'])
    subprocess.call(["SnippingTool.exe", '/clip'])
    clipboard_data = ImageGrab.grabclipboard()
    #clipboard_data.save(path + name)
    return clipboard_data

def image_to_base64(image):
    """
    Turns an image into a byte string
    Uses a buffer to load  the image from image object, since .tobytes from PIL Image returns the raw data(instead of compressed webp)
    Checks if the image is empty and translates it to ""
    :param image: PIL image
    :return: image encoded to base64 string
    """
    h, w = image.size
    if h == 1 or w == 1:
        return ""
    webp_buffer = BytesIO()
    image.save(webp_buffer, format=image.format)
    #image.convert("RGB").save(webp_buffer, format="WEBP")
    img_base64 = base64.b64encode(webp_buffer.getvalue()).decode("utf-8")
    return img_base64

def base64_to_image(base64_data):
    """
    Turns a byte string into an image.
    Uses a buffer to convert the data into an image object.
    :param base64_data: image encoded to base64 string
    :return: PIL image
    """
    if(base64_data) == "":
        return Image.new('RGB', (1, 1), (255, 255, 255))
    image_data = base64.b64decode(base64_data.encode("utf-8"))
    image_buffer = BytesIO(image_data)
    image = Image.open(image_buffer)
    return image

def get_window_position(window):
    """ Get the position of a Tkinter window. """
    return [int(coord) for coord in window.geometry().split('+')[1:]]

def center_window(over_window, window_to_center, window_width, window_height):
    """ Center `window_to_center` over `over_window` """
    over_window.update_idletasks()
    over_window.update()
    window_to_center.update_idletasks()
    window_to_center.update()

    # Get the size and position of the main window
    root_x = over_window.winfo_x()
    root_y = over_window.winfo_y()
    root_width = over_window.winfo_width()
    root_height = over_window.winfo_height()
    print("root_x", root_x, "root_y", root_y, "root_width", root_width, "root_height", root_height)

    # Get the size of the window to center
    print("window_width", window_width, "window_height", window_height)

    # Calculate the position to center the window
    center_x = root_x + (root_width - window_width) // 2
    center_y = root_y + (root_height - window_height) // 2

    # Set the position of the window
    window_to_center.geometry(f"+{center_x}+{center_y}")