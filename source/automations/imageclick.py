import pyautogui  # https://pyautogui.readthedocs.io/en/latest/screenshot.html
# import cv2  #https://docs.opencv.org/4.x/d1/dfb/intro.html
import time

# from functools import partial #library for multi screen
# ImageGrab.grab = partial(ImageGrab.grab, all_screens=True) #fix for no multi screen support
# Folder location: C:\Users\John\AppData\Local\Programs\Python\Python311\Lib\site-packages

from source.utility.miscfunctions import *


class ImageClick:
    def __init__(self):
        self.img = Image.new('RGB', (1, 1), (255, 255, 255))
        self.imgName = ""

    def set_img(self, img):
        self.img = img

    def set_img_name(self, imgName):
        self.imgName = imgName

    def unset_img(self):
        self.img = Image.new('RGB', (1, 1), (255, 255, 255))

    def unset_img_name(self):
        self.imgName = ""

    def do_click(self):
        button = pyautogui.locateOnScreen(self.img)  # check exception after
        # i=0.9
        # while button != ImageNotFoundException and i != 0.5:
        #    button = pyautogui.locateOnScreen(image, confidence=i)
        #    i=i-0.05
        if button is None:
            return
        button_point = pyautogui.center(button)
        pyautogui.click(button_point.x, button_point.y)

    def return_dictionary(self):
        return {'type': 'imageClick', 'imgName': self.imgName, 'image': image_to_base64(self.img)}

    def play(self):
        if self.imgName == "":
            return
        self.do_click()

def create_via_dictionary(dictionary):
    obj=ImageClick()
    obj.set_img_name(dictionary['imgName'])
    obj.set_img(base64_to_image(dictionary['image']))
    return obj


def repeat_till_success(image, maxSeconds):
    button = None
    tries = 0
    while button == None:
        button = pyautogui.locateOnScreen(image)
        print(button, tries)
        time.sleep(0.5)
        tries = tries + 0.5
        if tries == maxSeconds:
            return
    buttonPoint = pyautogui.center(button)
    pyautogui.click(buttonPoint.x, buttonPoint.y)


def repeat_till_success1(image, maxSeconds):
    button = None
    tries = 0
    while button == None:
        button = pyautogui.locateOnScreen(image)
        if button == None:
            button = pyautogui.locateOnScreen('screenshot11.PNG')
        print(button, tries)
        time.sleep(0.5)
        tries = tries + 0.5
        if tries == maxSeconds:
            return
    buttonPoint = pyautogui.center(button)
    pyautogui.click(buttonPoint.x, buttonPoint.y)


def try_till_success(image):
    button = None
    percent = 1
    while button == None and percent != 0.89:
        button = pyautogui.locateOnScreen(image, confidence=percent)
        percent = percent - 0.01
    buttonPoint = pyautogui.center(button)
    pyautogui.click(buttonPoint.x, buttonPoint.y)



# do_click('screenshot2.PNG', 10)
# seconds1 = get_seconds_delay()
# seconds2 = get_seconds_delay()
# seconds3 = get_seconds_delay()
"""

seconds1=10
seconds2=15
seconds3=5
seconds4=180
j = 0
while j < 125:
    repeat_till_success1('screenshot1.PNG', 30)
    time.sleep(1)
    repeat_till_success('screenshot2.PNG', 30)
    time.sleep(1)
    #do_click('screenshot3.PNG', seconds3)
    #do_click('screenshot4.PNG', seconds4)
    repeat_till_success('screenshot4.PNG', 180)
    time.sleep(5)
    j=j+1


# if


print("Screenshot captured successfully.")

# Get the active window
window = gw.getActiveWindow()

# Bring the window to the front (optional)
window.activate()

# Wait for the user to click and drag to select a region
print("Click and drag to select a region on the screen...")
region = window.getBox()

# Capture the screenshot of the selected region
screenshot = ImageGrab.grab(region)

# Save the screenshot to a file
screenshot.save('screenshot.png')
print("Screenshot captured successfully.")
time.sleep(1000000)

subprocess.call([r'C:\\Windows\System32\SnippingTool.exe', '/clip'])
clipboard_data = ImageGrab.grabclipboard()
clipboard_data.save('screenshot1.PNG')
subprocess.call([r'C:\\Windows\System32\SnippingTool.exe', '/clip'])
clipboard_data = ImageGrab.grabclipboard()
clipboard_data.save('screenshot2.PNG')
subprocess.call([r'C:\\Windows\System32\SnippingTool.exe', '/clip'])
clipboard_data = ImageGrab.grabclipboard()
clipboard_data.save('screenshot3.PNG')





def get_seconds_delay():
    root.withdraw()  # Hide the root window

    # Display an input dialog box and retrieve user input
    user_input = simpledialog.askstring("User Input", "Enter seconds till click:")

    if user_input is None:
        return None
    else:
        return user_input
"""

#get_cut_image()
#print(image_open_to_base64('test.PNG'))