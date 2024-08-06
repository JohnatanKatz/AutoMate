import tkinter as tk
import customtkinter as ctk
from source.utility.toast import show_toast
#from windowdynamicsui import WindowDynamicsUI
from source.ui.autogridobject import AutoGridUI, AutoGridData
import source.ui.config as config


def trace_callback(*args):
    print("Variable changed:", args)
class FileDataError(Exception):
    pass

class ButtonRowApp:
    def __init__(self, root):
        ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
        self.root = root
        #program data intilization
        grid_data = AutoGridData()

        self.root.title("AutoMate")
        self.root.wm_geometry(f"{1000}x{580}")

        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=0)
        self.root.grid_rowconfigure(0, weight=1)

        #sidebar initialization
        sidebar_frame = ctk.CTkFrame(self.root, width=140, corner_radius=0, fg_color="#2A2A2A")
        sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        sidebar_frame.grid_rowconfigure(6, weight=1)
        primary_color = "#007BFF"
        logo_label = ctk.CTkLabel(sidebar_frame, text="AutoMate", text_color=primary_color, font=ctk.CTkFont(size=20, weight="bold"), anchor="center")
        logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        #Sidebar Buttons for differnt program options
        main_grid = AutoGridUI(root, grid_data)
        sidebar_load = ctk.CTkButton(sidebar_frame, text="Load", command=lambda: main_grid.load_ui())
        sidebar_load.grid(row=1, column=0, padx=20, pady=10)
        sidebar_save = ctk.CTkButton(sidebar_frame, text="Save", command=lambda: main_grid.save_ui()) #fg_color=config.COLOR_PRIMARY
        sidebar_save.grid(row=2, column=0, padx=20, pady=10)
        sidebar_play_all = ctk.CTkButton(sidebar_frame, text="Play All", command=lambda: main_grid.play_all())
        sidebar_play_all.grid(row=3, column=0, padx=20, pady=10)

        #Sidebar repeat input
        pause_variable = tk.StringVar(value=str(1))  # default 1
        scaling_label = ctk.CTkLabel(sidebar_frame, text="Total repeats:")
        scaling_label.grid(row=4, column=0, padx=20, pady=(10, 0))
        program_repeats = ctk.CTkEntry(sidebar_frame, textvariable=pause_variable)
        program_repeats.configure(width=60)
        program_repeats.grid(row=5, column=0, padx=20, pady=10)
        program_repeats.bind("<FocusOut>", lambda event, widget=program_repeats: main_grid.set_program_repeat(event, widget))
        program_repeats.bind("<Return>", lambda event, widget=program_repeats: main_grid.set_program_repeat(event, widget))

        #Sidebar UI scaling feature
        scaling_label = ctk.CTkLabel(sidebar_frame, text="UI Scaling:", anchor="w")
        scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        scaling_optionemenu = ctk.CTkOptionMenu(sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))



    """"
        appearance_mode_label = ctk.CTkLabel(sidebar_frame, text="Appearance Mode:", anchor="w")
        appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        appearance_mode_optionemenu = ctk.CTkOptionMenu(sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        
    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
        """
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)