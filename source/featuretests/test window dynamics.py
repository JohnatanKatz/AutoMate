import pyautogui
import win32gui
import win32con


def get_window_under_cursor():
    # Get the cursor's current position
    x, y = pyautogui.position()

    # Find the window under the cursor
    hwnd = win32gui.WindowFromPoint((x, y))

    return hwnd


def maximize_window(hwnd):
    # Maximize the window
    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)


try:
    while True:
        # Wait for a mouse click
        pyautogui.click()

        # Get the window under the cursor
        hwnd = get_window_under_cursor()

        # Maximize the clicked window
        if hwnd:
            maximize_window(hwnd)
except KeyboardInterrupt:
    pass
