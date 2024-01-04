from lineui import GenericLineUI
import customtkinter as ctk
from source.automations.macro import Macro
from source.utility.filehandler import get_asset


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
            [self.new_row_number_entry, macro_input, self.dropdown, self.repeat_entry, self.pause_entry,
             self.delete_button])
        data = {'object': Macro(), 'option': row_data['option'], 'repeat': row_data['repeat'], 'pause': row_data['pause']}
        self.grid_data.data_rows.append(data)

    def record_macro(self, widget):
        """

        :param widget:
        :return:
        """

        info = widget.grid_info()
        index = int(info["row"]) - 1
        self.root.withdraw()
        self.grid_data.data_rows[index]['object'].record()
        self.root.deiconify()
        self.root.focus_set()

        # create UI Object
        macro_input = ctk.CTkFrame(self.scrollable_frame)
        macro_input.grid(row=index + 1, column=1, padx=0, pady=0)

        cancel_icon = get_asset('cancel_icon.png')  # macro.open('AutoMate/assets/delete_icon.svg')
        cancel_icon = ctk.CTkImage(cancel_icon)
        macro_widget_name = ctk.CTkButton(macro_input, text="", image=cancel_icon, compound="right")
        macro_widget_name.configure(command=lambda widget=macro_input: self.unset_macro(widget))
        macro_widget_name.pack(side=ctk.LEFT, padx=4, pady=4)

        # Open file icon button (Replace with your icon)
        play_button = ctk.CTkButton(macro_input, text="Play")
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
        self.grid_data.widget_rows[index].insert(1, macro_input)