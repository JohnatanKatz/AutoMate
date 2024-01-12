import tkinter as tk
import customtkinter as ctk
from source.utility.filehandler import get_asset
import source.ui.config as config

class GenericLineUI:

    def __init__(self, scrollable_frame, row_data, grid_data, root):
        """
        And gives the user the ability to account for two or more different buttons being used for the same proccess. It
        loops around between the current line and the next one, till they're out of repeats.

        Skip gives the user the ability to skip a line without deleting it.
        """
        self.grid_data=grid_data
        self.root=root
        self.scrollable_frame=scrollable_frame
        self.row_number = len(self.grid_data.widget_rows) + 1

        row_number_var = tk.StringVar(value=str(self.row_number))

        # Numerical input field for changing row position
        self.new_row_number_entry = ctk.CTkEntry(scrollable_frame, textvariable=row_number_var)
        self.new_row_number_entry.configure(width=40)
        self.new_row_number_entry.grid(row=self.row_number, column=0, padx=8, pady=8)
        self.new_row_number_entry.bind("<FocusOut>",
                                  lambda event, widget=self.new_row_number_entry: self.update_row_position(event, widget))
        self.new_row_number_entry.bind("<Return>",
                                  lambda event, widget=self.new_row_number_entry: self.update_row_position(event, widget))

        options = ["Normal", "And", "Skip"]
        dropdown_var = tk.StringVar(scrollable_frame)
        dropdown_var.set(row_data['option'])  # default Normal
        self.dropdown = ctk.CTkOptionMenu(scrollable_frame, values=options, width=100)
        self.dropdown.grid(row=self.row_number, column=2, padx=8, pady=8)

        # Repeat Input
        repeat_variable = tk.StringVar(value=str(row_data['repeat']))  # default 1

        self.repeat_entry = ctk.CTkEntry(scrollable_frame, textvariable=repeat_variable)
        self.repeat_entry.configure(width=60)
        self.repeat_entry.grid(row=self.row_number, column=3, padx=8, pady=8)
        self.repeat_entry.bind("<FocusOut>", lambda event, widget=self.repeat_entry: self.set_repeat(event, widget))
        self.repeat_entry.bind("<Return>", lambda event, widget=self.repeat_entry: self.set_repeat(event, widget))

        # Pause Input
        pause_variable = tk.StringVar(value=str(row_data['pause']))  # default 0

        self.pause_entry = ctk.CTkEntry(scrollable_frame, textvariable=pause_variable)
        self.pause_entry.configure(width=60)
        self.pause_entry.grid(row=self.row_number, column=4, padx=8, pady=8)
        self.pause_entry.bind("<FocusOut>", lambda event, widget=self.pause_entry: self.set_pause(event, widget))
        self.pause_entry.bind("<Return>", lambda event, widget=self.pause_entry: self.set_pause(event, widget))

        #Description
        self.description_button = ctk.CTkButton(scrollable_frame, text="View", width=100)
        self.description_button.configure(command=lambda widget=self.description_button: self.description(widget))
        self.description_button.grid(row=self.row_number, column=5, padx=8, pady=8)

        # Delete button
        del_icon = get_asset('delete_icon.png')  # Image.open('AutoMate/assets/delete_icon.svg')
        del_icon = ctk.CTkImage(del_icon)
        self.delete_button = ctk.CTkButton(scrollable_frame, text="", image=del_icon, width=0)
        self.delete_button.configure(command=lambda widget=self.delete_button: self.delete_row(widget))
        self.delete_button.grid(row=self.row_number, column=6, padx=8, pady=8)


    def set_repeat(self, event, widget):
        info = widget.grid_info()
        index = int(info["row"]) - 1
        if not ((event.type == tk.EventType.FocusOut) or (
                event.type == tk.EventType.KeyPress and event.keysym == 'Return')):
            raise Exception("Event type is not <FocusOut> or <Return> instead:", event)  # change to external library error.
        if not (widget.get().isdigit()):
            widget.delete(0, ctk.END)
            widget.insert(0, index)
            self.root.focus_set()
            return
        self.grid_data.data_rows[index]['repeat'] = int(widget.get())
        self.root.focus_set()

    def set_pause(self, event, widget):
        info = widget.grid_info()
        index = int(info["row"]) - 1
        if not ((event.type == tk.EventType.FocusOut) or (
                event.type == tk.EventType.KeyPress and event.keysym == 'Return')):
            raise Exception("Event type is not <FocusOut> or <Return>")  # change to external library error.
        if not (widget.get().isdigit()):
            widget.delete(0, ctk.END)
            widget.insert(0, index)
            self.root.focus_set()
            return
        self.grid_data.data_rows[index]['pause'] = int(widget.get())
        self.root.focus_set()

    def delete_row(self, widget):
        info = widget.grid_info()
        index = int(info["row"]) - 1
        print("Deleting row", index,"length", len(self.grid_data.widget_rows))
        for widget in self.grid_data.widget_rows[index]:
            widget.destroy()
        del self.grid_data.widget_rows[index]
        del self.grid_data.data_rows[index]
        if index != len(self.grid_data.widget_rows):  # If the deleted row was not the last row
            self.rearrange_rows(index-1)

    def play_button_func(self, widget):
        info = widget.grid_info()
        index = int(info["row"]) - 1
        self.root.withdraw()
        self.grid_data.data_rows[index]['object'].play()
        self.root.deiconify()
        self.root.focus_set()

    def update_row_position(self, event, widget):
        """

        Edge cases accounted for:
        1. Other than number Entered, simply delete it.
        2. index is higher or lower than max and min, set it to max/min instead.
        3. index is at same position, simply do nothing.
        :param event:
        :param widget:
        :return:
        """
        info = widget.grid_info()
        index = int(info["row"]) - 1
        print(len(self.grid_data.widget_rows))
        print(index, widget.get())
        if not ((event.type == tk.EventType.FocusOut) or (
                event.type == tk.EventType.KeyPress and event.keysym == 'Return')):
            raise Exception("Event type is not <FocusOut> or <Return>", event) # change to external library error.
        if not(widget.get().isdigit()):
            print("exit1")
            widget.delete(0, ctk.END)
            widget.insert(0, index+1)
            self.root.focus_set()
            return

        new_position = int(widget.get()) - 1
        if index == new_position or new_position < 1:  #Same position or negative, do nothing.
            print("exit2")
            print(new_position, index)
            widget.delete(0, ctk.END)
            widget.insert(0, index+1)
            self.root.focus_set()
            return
        if new_position > len(self.grid_data.widget_rows) - 1:
            print("exit3")
            print(new_position, index)
            widget.delete(0, ctk.END)
            widget.insert(0, str(len(self.grid_data.widget_rows)))
            new_position = len(self.grid_data.widget_rows) - 1
        print("inserting", widget.get())
        print("Moving row", index, "to position", new_position)
        print(self.grid_data.widget_rows)
        print(self.grid_data.data_rows)
        self.grid_data.data_rows.insert(new_position, self.grid_data.data_rows.pop(index))
        self.grid_data.widget_rows.insert(new_position, self.grid_data.widget_rows.pop(index))
        print(self.grid_data.data_rows)
        print(self.grid_data.widget_rows)
        self.rearrange_rows(min(index, new_position))
        self.root.focus_set()
        #self.rearrange_rows(0)


    def rearrange_rows(self, index):
        print("Rearranging rows", index)
        while index < len(self.grid_data.widget_rows):
            print("redoing",index)
            for col, widget in enumerate(self.grid_data.widget_rows[index]):
                print("col", col, "widget", widget, "length", len(self.grid_data.widget_rows[index]))
                if col == 0:
                    widget.delete(0, ctk.END)
                    widget.insert(0, index+1)
                widget.grid(row=index+1, column=col)
            index = index + 1
            print(self.grid_data.widget_rows)

    def description(self, widget):
        def save_text():
            updated_text = text_area.get("1.0", "end-1c")
            self.grid_data.data_rows[index]['description']=updated_text
            description_window.destroy()

        info = widget.grid_info()
        index = int(info["row"]) - 1

        description_window = ctk.CTkToplevel(self.root)
        description_window.title("Simple Text Editor")
        description_window.geometry("600x400")
        description_window.transient(self.root)

        print(self.grid_data.data_rows[index])
        text_content = self.grid_data.data_rows[index]['description']

        text_frame = ctk.CTkFrame(description_window)
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)

        text_area = ctk.CTkTextbox(text_frame, width=500, height=300, wrap="word")
        text_area.pack(side="left", fill="both", expand=True)

        scrollbar = ctk.CTkScrollbar(text_frame, command=text_area.yview)
        scrollbar.pack(side="right", fill="y")

        text_area.configure(yscrollcommand=scrollbar.set)
        text_area.insert("1.0", text_content)

        save_button = ctk.CTkButton(description_window, text="Save and Close", command=save_text)
        save_button.pack(pady=10)




