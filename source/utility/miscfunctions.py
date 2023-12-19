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