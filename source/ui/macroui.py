from source.ui.lineui import GenericLineUI
import customtkinter as ctk
from source.automations.macro import Macro
from source.utility.filehandler import get_asset
import source.utility.miscfunctions as miscfunctions
import source.ui.config

class MacroUI(GenericLineUI):
    def __init__(self, scrollable_frame, row_data, grid_data, root):
        super().__init__(scrollable_frame, row_data, grid_data, root)

        macro_input = ctk.CTkFrame(scrollable_frame)
        macro_input.grid(row=self.row_number, column=1, padx=0, pady=0)

        record_button = ctk.CTkButton(macro_input, text="Record")
        record_button.configure(command=lambda widget=macro_input: self.record_macro(widget))
        # screen_cut_button.grid(row=row_number, column=1, padx=4, pady=4)
        record_button.pack(anchor = 'center', padx=4, pady=4)

        self.grid_data.widget_rows.append(
            [self.new_row_number_entry, macro_input, self.dropdown, self.repeat_entry, self.pause_entry, self.description_button,
             self.delete_button])
        data = {'object': Macro(), 'option': row_data['option'], 'repeat': row_data['repeat'], 'pause': row_data['pause'], 'description': row_data['description']}
        self.grid_data.data_rows.append(data)

    def record_macro(self, widget):
        info = widget.grid_info()
        index = int(info["row"]) - 1
        self.root.withdraw()
        self.grid_data.data_rows[index]['object'].record()
        self.root.deiconify()
        self.root.focus_set()
        self.set_macroUI(index)

    def set_macroUI(self, index):
        """

        :param widget:
        :return:
        """

        # create UI Object
        macro_input = ctk.CTkFrame(self.scrollable_frame)
        macro_input.grid(row=index + 1, column=1, padx=0, pady=0)

        # Screen cut icon button (Replace with your icon)
        image_widget_name = ctk.CTkButton(macro_input, text="Macro", compound="right", width=100)
        image_widget_name.configure(command=lambda widget=macro_input: self.view_object(widget))
        image_widget_name.pack(side=ctk.LEFT, padx=(4, 0), pady=4)

        cancel_icon = get_asset('cancel_icon.png')  # macro.open('AutoMate/assets/delete_icon.svg')
        cancel_icon = ctk.CTkImage(cancel_icon)
        macro_widget_name = ctk.CTkButton(macro_input, text="", image=cancel_icon, compound="right", width=0)
        macro_widget_name.configure(command=lambda widget=macro_input: self.unset_macro(widget))
        macro_widget_name.pack(side=ctk.LEFT, padx=4, pady=4)

        # Open file icon button (Replace with your icon)
        play_button = ctk.CTkButton(macro_input, text="Play", width=100)
        play_button.configure(command=lambda widget=macro_input: self.play_button_func(widget))
        play_button.pack(side=ctk.RIGHT, padx=4, pady=4)

        # Save to the UI
        self.grid_data.widget_rows[index][1].destroy()
        self.grid_data.widget_rows[index].pop(1)
        self.grid_data.widget_rows[index].insert(1, macro_input)

    def unset_macro(self, widget):
        """
        Removes the macro from the UI and the macroClick object
        :param widget: used to get the widgets' index on the grid
        """
        info = widget.grid_info()
        index = int(info["row"]) - 1
        self.grid_data.data_rows[index]['object'].unset_events()

        macro_input = ctk.CTkFrame(self.scrollable_frame)
        macro_input.grid(row=index + 1, column=1, padx=0, pady=0)

        record_button = ctk.CTkButton(macro_input, text="Record")
        record_button.configure(command=lambda widget=macro_input: self.record_macro(widget))
        # screen_cut_button.grid(row=row_number, column=1, padx=4, pady=4)
        record_button.pack(anchor = 'center', padx=4, pady=4)

        self.grid_data.widget_rows[index][1].destroy()
        self.grid_data.widget_rows[index].pop(1)
        self.grid_data.widget_rows[index].insert(1, macro_input)


    def view_object(self, widget):
        if hasattr(self, 'macro_window') and self.macro_window.winfo_exists():
            self.macro_window.focus_set()
            return
        info = widget.grid_info()
        index = int(info["row"]) - 1
        self.macro_window = ctk.CTkToplevel(self.root)

        self.macro_window.title("Macro Display")
        self.macro_window.wm_geometry(f"{400}x{450}")
        self.macro_window.withdraw()

        # Get the macro's text content
        macro_text = self.grid_data.data_rows[index]['object'].return_dictionary()

        # Create a Textbox to display the macro's text content
        text_frame = ctk.CTkFrame(self.macro_window)
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)

        text_area = ctk.CTkTextbox(text_frame, width=500, height=300, wrap="word")
        text_area.pack(side="left", fill="both", expand=True)

        scrollbar = ctk.CTkScrollbar(text_frame, command=text_area.yview)
        scrollbar.pack(side="right", fill="y")

        text_area.configure(yscrollcommand=scrollbar.set)
        text_area.insert("1.0", macro_text)

        miscfunctions.center_window(self.root, self.macro_window, 400, 450)
        self.macro_window.deiconify()