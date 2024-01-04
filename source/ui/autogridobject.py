import customtkinter as ctk
from source.utility.filehandler import load, save
import source.automations.imageclick as imageclick
import source.automations.macro as macro
import source.automations.windowdynamics as windowdynamics
from macroui import MacroUI
from imageclickui import ImageClickUI
import time

class AutoGridData:
    def __init__(self):
        self.image_count = 1
        self.loop_repetitions = 0
        self.widget_rows = []  # List of rows containing widgets
        self.data_rows = []  # List of rows containing Macro objects or ImageClick objects


class AutoGridUI:
    def __init__(self, root, grid_data):

        self.root=root
        self.grid_data = AutoGridData()
        default_row_data = {'option': "Normal", 'repeat': 1,
                            'pause': 0}

        self.scrollable_frame = ctk.CTkScrollableFrame(self.root, label_text="CTkScrollableFrame")
        self.scrollable_frame.grid(row=0, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)



        ImageClickUI(self.scrollable_frame, default_row_data, self.grid_data, root)

        # title_label = ctk.CTkLabel(self.scrollable_frame, text="Full Repetitions")
        # title_label.grid(row=0, column=3, padx=4, pady=4)
        title_label = ctk.CTkLabel(self.scrollable_frame, text="Runtime")
        title_label.grid(row=0, column=2, padx=4, pady=4)
        title_label = ctk.CTkLabel(self.scrollable_frame, text="Repetitions")
        title_label.grid(row=0, column=3, padx=4, pady=4)
        title_label = ctk.CTkLabel(self.scrollable_frame, text="Pause S")
        title_label.grid(row=0, column=4, padx=4, pady=4)

        grid_button = ctk.CTkFrame(self.root)
        grid_button.grid(row=1, column=1)  # padx=8, pady=8)

        add_row_button = ctk.CTkButton(grid_button, text="Add Image Recognition",
                                       command=lambda: ImageClickUI(self.scrollable_frame, default_row_data, self.grid_data, root))
        add_row_button.grid(row=0, column=0, padx=10, pady=10)
        add_row_button = ctk.CTkButton(grid_button, text="Add Macro",
                                       command=lambda: MacroUI(self.scrollable_frame, default_row_data, self.grid_data, root))
        add_row_button.grid(row=0, column=1, padx=10, pady=10)
        add_row_button = ctk.CTkButton(grid_button, text="Play all", command=lambda: self.play_all())
        add_row_button.grid(row=0, column=2, padx=10, pady=10)

    def play_all(self):
        """
        This function handles running the entire loop.
        It prepares every object that need to run togather, checked via the And argument, in lists within the main list to loop over.
        It stores the repeats for each object into a separate array to keep count of number of runs without changing the program data.

        Once the data is prepared it loops over the entire list of lists until the total repeats is 0. While running every object.
        """
        repeat_counter = []
        and_repeat_array = []
        and_array = []
        play_all_array = []
        for row in self.grid_data.data_rows: #prepares
            print(row)
            if row['option']=="And":
                and_array.append(row)
                repeat_counter.append(row['repeat'])
            elif row['option']!="Skip":
                and_array.append(row)
                play_all_array.append(and_array)
                and_array = []
                repeat_counter.append(row['repeat'])
                and_repeat_array.append(repeat_counter)
                repeat_counter = []
        print("lel")
        for object_array, repeat_array in zip(play_all_array, and_repeat_array):
            print("test")
            print(object_array, repeat_array)
            i = 0
            while sum(repeat_array)>0:
                print("repeat", repeat_array)
                if i==len(object_array):
                    i=0
                if repeat_array[i]>0:
                    repeat_array[i]=-1
                    print("play")
                    object_array[i]['object'].play()
                    time.sleep(object_array[i]['pause'])


    def load_ui(self):
        """
        The function uses the data read from a saved file to set each row in our data grid
        For each line of data it checks the object type and calls the apropriate initation function for it.
        :return:
        """
        data=load(self.root)
        if data is None:
            return
        self.clear_all_rows()
        self.loop_repetitions=data['loop_repetitions']
        i=0
        for row in data['data_rows']:
            row_data = {'option': row['option'], 'repeat': row['repeat'], 'pause': row['pause']}
            if row['object']['type'] == 'imageClick':
                ImageClickUI(self.scrollable_frame, row_data, self.grid_data, self.root)
                self.grid_data.data_rows[i]['object'] = imageclick.create_via_dictionary(row['object'])
                if row['object']['imgName']!="":
                    ImageClickUI.set_image_ui(i, row['object']['imgName'])
            elif row['object']['type'] == 'macro':
                MacroUI(self.scrollable_frame, row_data, self.grid_data, self.root)
                self.grid_data.data_rows[i]['object'] = macro.create_via_dictionary(row['object'])
            i=+1
        self.loop_repetitions = data['loop_repetitions']

    def save_ui(self):
        save(self.grid_data.data_rows, self.grid_data.loop_repetitions, self.root)

    def clear_all_rows(self):
        self.grid_data.data_rows = []
        for row in self.grid_data.widget_rows:
            for widget in row:
                widget.destroy()
        self.grid_data.widget_rows = []