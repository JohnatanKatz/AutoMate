from tkinter import filedialog
import tkinter as tk
import threading
import json
import os
from PIL import Image

from source.utility import toast


def save(data_rows, loop_repetitions, root):
    """
    Saves the instance to file by:
    Removes the image from the UI and the ImageClick object
    Goes over
    Attaches togather the data, and saves it to a json file.
    :param root: The main window to draw a toast on if there is an error.
    :return:
    """
    rootsave = tk.Tk()
    rootsave.withdraw()  # Hide the main window
    try:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
    except Exception as e:
        # Add potential log here
        toast_thread = threading.Thread(target=toast.show_toast(root, "Unable to save file. Please check the file path or try again."))
        toast_thread.start()
        return
    rootsave.destroy()
    if file_path == "":
        return
    print(len(data_rows), "length")
    data_rows_save = []
    for row in data_rows:
        data_rows_save.append({'object': row['object'].return_dictionary(), 'option': row['option'],
                               'repeat': row['repeat'], 'pause': row['pause']})
    data_save={'data_rows': data_rows_save, 'loop_repetitions': loop_repetitions}
    with open(file_path, "w") as file:
        json.dump(data_save, file, indent=4)

#def export(data_rows):

#def quick_save()

def load(root):
    """

    :param root: The main window to draw a toast on if there is an error.
    :return:
    """
    rootsave = tk.Tk()
    rootsave.withdraw()  # Hide the main window
    try:
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
    except Exception as e:
        # Add potential log here
        toast_thread = threading.Thread(target=toast.show_toast(root, "Unable to load file. Please check the file path or try again."))
        toast_thread.start()
        return None
    rootsave.destroy()
    if file_path == "":  # user cancels
        return None
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            return data
    except Exception as e:
        toast_thread = threading.Thread(target=toast.show_toast(root, "File data is corrupted"))
        toast_thread.start()
        return None

#def import():

def get_asset(asset_name):
    # Get the path to the "assets" folder relative to the current script or program
    root_directory = os.path.dirname(os.path.dirname(os.getcwd()))
    folder_name = 'assets'
    image_path = os.path.join(root_directory, folder_name, asset_name)
    print(image_path)
    try:
        image = Image.open(image_path)
        print(image)
        return image
    except FileNotFoundError:
        print(f"Image file not found: {image_path}") #temp
    except Exception as e:
        print(f"An error occurred: {e}") #temp

