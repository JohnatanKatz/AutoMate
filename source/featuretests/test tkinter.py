import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

def create_scrollable_frame(parent):
    canvas = tk.Canvas(parent)
    scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    return scrollable_frame

def add_row():
    new_row = ttk.Frame(main_frame)
    new_row.pack(padx=10, pady=10, fill="both")

    button_text = f"Button {len(button_list) + 1}"
    button_list.append(button_text)

    button = ttk.Button(new_row, text=button_text)
    button.pack(side="left")

    checkbox_var = tk.BooleanVar(value=False)
    checkbox = ttk.Checkbutton(new_row, text="Checkbox", variable=checkbox_var)
    checkbox.pack(side="left", padx=10)

    dropdown_var = tk.StringVar(value="Option 1")
    dropdown_menu = ttk.Combobox(new_row, values=["Option 1", "Option 2", "Option 3"], textvariable=dropdown_var)
    dropdown_menu.pack(side="left", padx=10)

    add_row_button.pack(pady=10, anchor="w", before=new_row)  # Move the "Add Row" button below the new row

def main():
    global main_frame, button_list, add_row_button
    root = tk.Tk()
    root.title("Scrollable GUI")

    main_frame = create_scrollable_frame(root)
    button_list = []

    label = tk.Label(main_frame, text="Scrollable GUI Example")
    label.pack(padx=10, pady=10)

    entry = ttk.Entry(main_frame)
    entry.pack(padx=10, pady=10)

    button = ttk.Button(main_frame, text="Click Me")
    button.pack(padx=10, pady=10)

    text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=40, height=10)
    text.insert("1.0", "This is a scrollable text area.")
    text.pack(padx=10, pady=10)

    button_list = [
        ("Button 1", "Option 1", "Option 2", "Option 3"),
        ("Button 2", "Option A", "Option B", "Option C"),
        ("Button 3", "Option X", "Option Y", "Option Z")
    ]

    for button_text, *dropdown_options in button_list:
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(padx=10, pady=10, fill="both")

        button = ttk.Button(button_frame, text=button_text)
        button.pack(side="left")

        checkbox_var = tk.BooleanVar(value=False)
        checkbox = ttk.Checkbutton(button_frame, text="Checkbox", variable=checkbox_var)
        checkbox.pack(side="left", padx=10)

        dropdown_var = tk.StringVar(value=dropdown_options[0])
        dropdown_menu = ttk.Combobox(button_frame, values=dropdown_options, textvariable=dropdown_var)
        dropdown_menu.pack(side="left", padx=10)

    add_row_button = ttk.Button(main_frame, text="Add Row", command=add_row)
    add_row_button.pack(pady=10, anchor="w")

    root.mainloop()

if __name__ == "__main__":
    main()
