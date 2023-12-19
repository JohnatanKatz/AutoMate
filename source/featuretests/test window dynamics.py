import pyautogui
import pygetwindow as gw
import time
import json


# Function to minimize or maximize windows
def minimize_or_maximize(window, action):
    if action == "minimize":
        window.minimize()
    elif action == "maximize":
        window.maximize()


# Function to prompt user for action and capture clicked window
def select_window():
    print("Please select an action (minimize or maximize).")
    action = input("Action: ").lower()
    while action not in ["minimize", "maximize"]:
        print("Invalid action. Please enter 'minimize' or 'maximize'.")
        action = input("Action: ").lower()

    print("Please click on the window you want to add or press 'Esc' to cancel.")

    while True:
        click_point = None

        while click_point is None:
            if pyautogui.onScreen(pyautogui.position()):
                click_point = pyautogui.position()
            time.sleep(0.1)  # Check for mouse click every 0.1 seconds

        target_window = gw.getWindowsAt(click_point[0], click_point[1])

        if target_window:
            return {"title": target_window[0].title, "action": action}
        else:
            print("No window found at the clicked location. Please try again or press 'Esc' to cancel.")


# Load existing configuration or create an empty list
try:
    with open("window_config.json", "r") as file:
        window_actions = json.load(file)
except FileNotFoundError:
    window_actions = []

# Prompt user for window selection and action
new_window = select_window()
if new_window:
    window_actions.append(new_window)

    # Save updated configuration to a JSON file
    with open("window_config.json", "w") as file:
        json.dump(window_actions, file)
