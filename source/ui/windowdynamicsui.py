from lineui import GenericLineUI
import customtkinter as ctk

class WindowDynamicsUI(GenericLineUI):
    def __init__(self, scrollable_frame, repeat, pause, grid_data, root):

def add_WindowAction_row(self, repeat, pause):
    row_number = len(self.widget_rows) + 1

    row_number_var = tk.StringVar(value=str(row_number))

    # Numerical input field for changing row position
    new_row_number_entry = ctk.CTkEntry(self.scrollable_frame, textvariable=row_number_var)
    new_row_number_entry.grid(row=row_number, column=0, padx=4, pady=4)
    new_row_number_entry.bind("<FocusOut>",
                              lambda event, widget=new_row_number_entry: self.update_row_position(event, widget))
    # row_number_var.trace("w", trace_callback)  # "w" stands for "write"

    self.data_rows.append(Macro())



#need to overwrite play in the parent class.