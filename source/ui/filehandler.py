from tkinter import filedialog
import tkinter as tk
import threading
import json

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
    print(data_save)
    with open(file_path, "w") as file:
        json.dump(data_save, file, indent=4)

#def export(data_rows):

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
        return ""
    rootsave.destroy()
    if file_path == "":  # user cancels
        return
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            return data
    except Exception as e:
        toast_thread = threading.Thread(target=toast.show_toast(root, "File data is corrupted"))
        toast_thread.start()
        return ""

#def import():
