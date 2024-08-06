import customtkinter as ctk
import tkinter as tk
from source.utility.filehandler import load, save
import source.automations.imageclick as imageclick
import source.automations.macro as macro
import source.automations.windowdynamics as windowdynamics
from source.ui.macroui import MacroUI
from source.ui.imageclickui import ImageClickUI
from source.ui.windowdynamicsui import WindowDynamicsUI
import time
import source.ui.config as config

class AutoGridData:
    def __init__(self):
        self.image_count = 1
        self.loop_repetitions = 0
        self.widget_rows = []  # List of rows containing widgets
        self.data_rows = []  # List of rows containing Macro objects or ImageClick objects


class AutoGridUI:
    def __init__(self, root, grid_data):
        # copilot please write me documentation for this function
        """
        The purpose of this function is to create the main grid for the user to add automations to.
        It is the main UI for the user to interact with the program.

        :param root: The tkinter root window
        :param grid_data: A class containing the data for the grid
        """

        self.root=root
        self.grid_data = AutoGridData()
        default_row_data = {'option': "Normal", 'repeat': 1,
                            'pause': 0, 'description': ""}
        self.program_repeats= 0
        self.scrollable_frame = ctk.CTkScrollableFrame(self.root, fg_color="#2A2A2A")
        #corner_radius=0
        self.scrollable_frame.grid(row=0, column=1, padx=(20, 0), pady=(0, 20), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)



        ImageClickUI(self.scrollable_frame, default_row_data, self.grid_data, root)

        title_label = ctk.CTkLabel(self.scrollable_frame, text="Index")
        title_label.grid(row=0, column=0, padx=4, pady=(20, 4))
        title_label = ctk.CTkLabel(self.scrollable_frame, text="Label required")
        title_label.grid(row=0, column=1, padx=4, pady=(20, 4))
        title_label = ctk.CTkLabel(self.scrollable_frame, text="Runtime")
        title_label.grid(row=0, column=2, padx=4, pady=(20, 4))
        title_label = ctk.CTkLabel(self.scrollable_frame, text="Repetitions")
        title_label.grid(row=0, column=3, padx=4, pady=(20, 4))
        title_label = ctk.CTkLabel(self.scrollable_frame, text="Pause(sec)")
        title_label.grid(row=0, column=4, padx=4, pady=(20, 4))
        title_label = ctk.CTkLabel(self.scrollable_frame, text="Description")
        title_label.grid(row=0, column=5, padx=4, pady=(20, 4))

        below_matrix = ctk.CTkFrame(self.root, fg_color="#2A2A2A")
        below_matrix.grid(row=1, column=1, sticky="nsew", padx=(20, 0), pady=0)

        add_label = ctk.CTkLabel(below_matrix, text="Add Automation:")
        add_label.pack(side="left", anchor="w", padx=8, pady=0)

        grid_button = ctk.CTkFrame(below_matrix, fg_color="#2A2A2A")
        grid_button.pack(side="right", anchor="e", padx=4, pady=4)

        add_row_button = ctk.CTkButton(grid_button, text="Image Recognition",
                                       command=lambda: ImageClickUI(self.scrollable_frame, default_row_data, self.grid_data, root))
        add_row_button.grid(row=0, column=0, padx=10, pady=10)
        add_row_button = ctk.CTkButton(grid_button, text="Macro",
                                       command=lambda: MacroUI(self.scrollable_frame, default_row_data, self.grid_data, root))
        add_row_button.grid(row=0, column=1, padx=10, pady=10)
        add_row_button = ctk.CTkButton(grid_button, text="Window",
                                       command=lambda: WindowDynamicsUI(self.scrollable_frame, default_row_data, self.grid_data,
                                                               root))
        add_row_button.grid(row=0, column=2, padx=10, pady=10)



        #Makes the grid evenly spaced
        num_columns = self.scrollable_frame.grid_size()[0]
        for i in range(num_columns):
            self.scrollable_frame.grid_columnconfigure(i, weight=1)

    def set_program_repeat(self, event, widget):
        info = widget.grid_info()
        index = int(info["row"]) - 1
        if not ((event.type == tk.EventType.FocusOut) or (
                event.type == tk.EventType.KeyPress and event.keysym == 'Return')):
            raise Exception("Event type is not <FocusOut> or <Return> instead:",
                            event)  # change to external library error.
        if not (widget.get().isdigit()):
            widget.delete(0, ctk.END)
            widget.insert(0, index)
            self.root.focus_set()
            return
        self.program_repeats = int(widget.get())
        self.root.focus_set()

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
            #print(row)
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
        """
        add a 0.5  or 0.2 second pause for the do until success option.
        self.root.withdraw()
        image = miscfunctions.get_cut_image()
        self.root.deiconify()
        self.root.focus_set()
        """
        #print("lel")
        self.root.withdraw()
        i = 0
        while self.program_repeats > i:
            for object_array, repeat_array in zip(play_all_array, and_repeat_array):
                #print("test")
                #print(object_array, repeat_array)
                i = 0
                while sum(repeat_array)>0:
                    #print("repeat", repeat_array)
                    if i==len(object_array):
                        i=0
                    if repeat_array[i]>0:
                        repeat_array[i]=repeat_array[i]-1
                        #print("play", repeat_array[i])
                        object_array[i]['object'].play()
                        time.sleep(object_array[i]['pause'])
            i=i+1
        self.root.deiconify()
        self.root.focus_set()


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
            print("loaded row data",row)
            row_data = {'option': row['option'], 'repeat': row['repeat'], 'pause': row['pause'], 'description': row['description']}
            if row['object']['type'] == 'imageClick':
                object=ImageClickUI(self.scrollable_frame, row_data, self.grid_data, self.root)
                self.grid_data.data_rows[i]['object'] = imageclick.create_via_dictionary(row['object'])
                if row['object']['imgName']!="":
                    object.set_image_ui(i, row['object']['imgName'])
            elif row['object']['type'] == 'macro':
                object=MacroUI(self.scrollable_frame, row_data, self.grid_data, self.root)
                self.grid_data.data_rows[i]['object'] = macro.create_via_dictionary(row['object'])
                if row['object']['events']!=[]:
                    object.set_macroUI(i)
            elif row['object']['type'] == 'windowDynamics':
                object=WindowDynamicsUI(self.scrollable_frame, row_data, self.grid_data, self.root)
                self.grid_data.data_rows[i]['object'] = windowdynamics.create_via_dictionary(row['object'])
                if row['object']['window']!="":
                    object.set_windowUI(i, row['object']['toggle'])
            i=i+1
        self.loop_repetitions = data['loop_repetitions']

    def save_ui(self):
        save(self.grid_data.data_rows, self.grid_data.loop_repetitions, self.root)

    def clear_all_rows(self):
        self.grid_data.data_rows = []
        for row in self.grid_data.widget_rows:
            for widget in row:
                widget.destroy()
        self.grid_data.widget_rows = []