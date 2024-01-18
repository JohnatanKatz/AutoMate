import os
from tkinter import filedialog
import tkinter as tk
from PIL import Image, ImageTk
from source.ui.lineui import GenericLineUI
import customtkinter as ctk
from source.utility.filehandler import get_asset
import threading
from source.automations.imageclick import ImageClick
from source.utility import miscfunctions
from source.utility.toast import show_toast
import source.ui.config as config

class ImageClickUI(GenericLineUI):
    def __init__(self, scrollable_frame, row_data, grid_data, root):
        """

        :param scrollable_frame:
        :param row_data: {'option': option, 'repeat': repeat, 'pause': pause}
        :param grid_data:
        :param root:
        """
        super().__init__(scrollable_frame, row_data, grid_data, root)
        # row_number_var.trace("w", trace_callback)  # "w" stands for "write"

        image_input = ctk.CTkFrame(scrollable_frame)
        image_input.grid(row=self.row_number, column=1, padx=0, pady=0)

        # Screen cut icon button (Replace with your icon)
        screen_cut_button = ctk.CTkButton(image_input, text="Screen Cut", width=100)
        screen_cut_button.configure(command=lambda widget=image_input: self.screen_shot(widget))
        # screen_cut_button.grid(row=row_number, column=1, padx=4, pady=4)
        screen_cut_button.pack(side=ctk.LEFT, padx=4, pady=4)

        # Open file icon button (Replace with your icon)
        open_file_button = ctk.CTkButton(image_input, text="Open File", width=100)
        open_file_button.configure(command=lambda widget=image_input: self.open_image(widget))
        # open_file_button.grid(row=row_number, column=2, padx=4, pady=4)
        open_file_button.pack(side=ctk.RIGHT, padx=4, pady=4)

        self.grid_data.widget_rows.append(
            [self.new_row_number_entry, image_input, self.dropdown, self.repeat_entry, self.pause_entry, self.description_button,
             self.delete_button])
        data = {'object': ImageClick(), 'option': row_data['option'], 'repeat': row_data['repeat'],
                'pause': row_data['pause'], 'description': row_data['description']}
        self.grid_data.data_rows.append(data)

    def open_image(self, widget):
        """
        Opens up the file viewer to select an image and passes it to the UI changing function.
        :param widget: used to get the widgets' index on the grid
        """
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("Image Files", "*.jpg *.jpeg *.png *apng *.webp *.bmp *.ppm *.pgm *.tiff *.tif")])
            image = Image.open(file_path)
            info = widget.grid_info()
            index = int(info["row"]) - 1
            name = os.path.basename(file_path)
            self.set_image(index, image, name)
            self.grid_data.image_count += 1
        except Exception as e:
            toast_thread = threading.Thread(target=show_toast(self.root, "Error opening the image"))
            toast_thread.start()
            return
            #log error here later {str(e)}

    def screen_shot(self, widget):
        """
        Calls a function that gets a specific screenshot of the screen and passes it to the UI changing function.
        :param widget: used to get the widgets' index on the grid
        """
        info = widget.grid_info()
        index = int(info["row"]) - 1
        self.root.withdraw()
        image = miscfunctions.get_cut_image()
        self.root.deiconify()
        self.root.focus_set()
        name="image"+str(self.grid_data.image_count)
        self.grid_data.image_count += 1
        self.set_image(index, image, name)

    def set_image(self, index, image, name):
        """

        :param index:
        :param image:
        :param name: the name of the image file
        """
        self.grid_data.data_rows[index]['object'].set_img(image)
        self.grid_data.data_rows[index]['object'].set_img_name(name)
        self.set_image_ui(index, name)

    def set_image_ui(self, index, name):
        display_name = name[:10]

        image_input = ctk.CTkFrame(self.scrollable_frame)
        image_input.grid(row=index + 1, column=1, padx=0, pady=0)

        # Screen cut icon button (Replace with your icon)
        image_widget_name = ctk.CTkButton(image_input, text=display_name, compound="right", width=100)
        image_widget_name.configure(command=lambda widget=image_input: self.view_image(widget))
        image_widget_name.pack(side=ctk.LEFT, padx=(4,0), pady=4)

        cancel_icon = get_asset('cancel_icon.png')  # Image.open('AutoMate/assets/delete_icon.svg')
        cancel_icon = ctk.CTkImage(cancel_icon)
        cancel_widget = ctk.CTkButton(image_input, text="", image=cancel_icon, compound="right", width=0)
        cancel_widget.configure(command=lambda widget=image_input: self.unset_image(widget))
        cancel_widget.pack(side=ctk.LEFT, padx=(4), pady=4)

        # Open file icon button (Replace with your icon)
        play_button = ctk.CTkButton(image_input, text="Play", width=100)
        play_button.configure(command=lambda widget=image_input: self.play_button_func(widget))
        play_button.pack(side=ctk.RIGHT, padx=4, pady=4)

        self.grid_data.widget_rows[index][1].destroy()
        self.grid_data.widget_rows[index].pop(1)
        self.grid_data.widget_rows[index].insert(1, image_input)
        self.root.update()

    def view_object(self, widget):
        if hasattr(self, 'object_window') and self.object_window.winfo_exists():
            self.object_window.focus_set()
            return
        info = widget.grid_info()
        index = int(info["row"]) - 1
        self.object_window = ctk.CTkToplevel(self.root)

        self.object_window.title("Image Display")
        self.object_window.wm_geometry(f"{400}x{450}")
        #self.object_window.attributes('-topmost', True)
        self.object_window.withdraw()

        #Convert the PIL image to a Tkinter-compatible photo image and scale it down to a 300 by 300 frame.
        original_image = self.grid_data.data_rows[index]['object'].get_image()
        max_size = (300, 300)
        original_image.thumbnail(max_size, Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(original_image)

        #Create Image Label
        image_label = tk.Label(self.object_window, image=photo, borderwidth=0, highlightthickness=0)
        image_label.image = photo
        image_label.pack(pady=10)

        #create name entry and button to set the new name
        name_entry = ctk.CTkEntry(self.object_window, placeholder_text="Enter image name")
        name_entry.insert(0, self.grid_data.data_rows[index]['object'].get_imgName())
        name_entry.pack(pady=10)
        set_name_button = ctk.CTkButton(self.object_window, text="Set New Name",
                                        command=lambda: self.set_new_name(self.grid_data.data_rows[index]['object'], name_entry))
        set_name_button.pack(pady=10)

        miscfunctions.center_window(self.root, self.object_window, 400, 450)
        self.object_window.deiconify()


    def set_new_name(self, image_click, name_entry):
        new_name = name_entry.get()
        image_click.set_img_name(new_name)
        print(f"New Image Name: {new_name}")


    def unset_image(self, widget):
        """
        Removes the image from the UI and the ImageClick object
        :param widget: used to get the widgets' index on the grid
        """
        info = widget.grid_info()
        index = int(info["row"]) - 1
        self.grid_data.data_rows[index]['object'].unset_img()
        self.grid_data.data_rows[index]['object'].unset_img_name()

        image_input = ctk.CTkFrame(self.scrollable_frame)
        image_input.grid(row=index+1, column=1, padx=0, pady=0)

        # Screen cut icon button (Replace with your icon)
        screen_cut_button = ctk.CTkButton(image_input, text="Screen Cut", width=100)
        screen_cut_button.configure(command=lambda widget=image_input: self.screen_shot(widget))
        # screen_cut_button.grid(row=row_number, column=1, padx=4, pady=4)
        screen_cut_button.pack(side=ctk.LEFT, padx=4, pady=4)

        # Open file icon button (Replace with your icon)
        open_file_button = ctk.CTkButton(image_input, text="Open File", width=100)
        open_file_button.configure(command=lambda widget=image_input: self.open_image(widget))
        # open_file_button.grid(row=row_number, column=2, padx=4, pady=4)
        open_file_button.pack(side=ctk.RIGHT, padx=4, pady=4)

        self.grid_data.widget_rows[index][1].destroy()
        self.grid_data.widget_rows[index].pop(1)
        self.grid_data.widget_rows[index].insert(1, image_input)