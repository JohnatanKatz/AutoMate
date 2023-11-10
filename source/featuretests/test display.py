import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import sv_ttk

class ButtonRowApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Button Row Example")

        self.grid_frame = ttk.Frame(self.root)
        self.grid_frame.pack(padx=8, pady=8)

        self.button_rows = []

        self.add_button_row()  # Initial button row

        add_row_button = ttk.Button(self.root, text="Add Row", command=self.add_button_row)
        add_row_button.pack(pady=8)

    def add_button_row(self):
        button_row = ttk.Frame(self.grid_frame)
        self.button_rows.append(button_row)

        row_number = len(self.button_rows)

        # Numerical input field for row number
        row_number_var = tk.IntVar(value=row_number)
        index_label = ttk.Label(button_row, textvariable=row_number_var)
        index_label.grid(row=row_number, column=0, padx=4, pady=4)

        # Screen cut icon button (Replace with your icon)
        screen_cut_button = ttk.Button(button_row, text="Screen Cut")
        screen_cut_button.grid(row=row_number, column=1, padx=4, pady=4)

        # Open file icon button (Replace with your icon)
        open_file_button = ttk.Button(button_row, text="Open File", command=self.open_file)
        open_file_button.grid(row=row_number, column=2, padx=4, pady=4)

        # Numerical input field for changing row position
        new_row_number_entry = ttk.Entry(button_row, textvariable=row_number_var)
        new_row_number_entry.grid(row=row_number, column=3, padx=4, pady=4)
        new_row_number_entry.bind("<FocusOut>", lambda event, index=row_number-1: self.update_row_position(event, index))

        # Dropdown
        options = ["Option 1", "Option 2", "Option 3"]  # Replace with your options
        dropdown_var = tk.StringVar(button_row)
        dropdown_var.set(options[0])
        dropdown = ttk.Combobox(button_row, textvariable=dropdown_var, values=options)
        dropdown.grid(row=row_number, column=4, padx=4, pady=4)

        # Delete button
        delete_button = ttk.Button(button_row, text="Delete", command=lambda index=row_number-1: self.delete_row(index))
        delete_button.grid(row=row_number, column=5, padx=4, pady=4)

        self.rearrange_rows()

    def update_row_position(self, event, index):
        new_position = event.widget.get()
        if new_position.isdigit():
            new_position = int(new_position)
            if 1 <= new_position <= len(self.button_rows):
                self.button_rows.insert(new_position - 1, self.button_rows.pop(index))
                self.rearrange_rows()

    def delete_row(self, index):
        print("Deleting row", index)
        print(self.button_rows)
        if 0 <= index < len(self.button_rows):
            self.button_rows[index].destroy()
            del self.button_rows[index]
            self.rearrange_rows()

    def rearrange_rows(self):
        for index, row in enumerate(self.button_rows):
            row.grid(row=index + 1)
            row.children['!label'].config(text=index + 1)

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            print("Selected file:", file_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = ButtonRowApp(root)

    sv_ttk.set_theme("dark")
    root.mainloop()
