import tkinter as tk


class MatrixLine(tk.Frame):
    def __init__(self, master, text, button_text):
        super().__init__(master)
        self.label = tk.Label(self, text=text)
        self.label.pack(side=tk.LEFT)

        self.button = tk.Button(self, text=button_text, command=self.on_button_click)
        self.button.pack(side=tk.LEFT)

    def on_button_click(self):
        print("Button clicked")


class RedLine(MatrixLine):
    def __init__(self, master):
        super().__init__(master, "Red Line - Hello", "Red Click")


class BlueLine(MatrixLine):
    def __init__(self, master):
        super().__init__(master, "Blue Line - Hello", "Blue Click")


class MatrixApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.matrix_frame = tk.Frame(self)
        self.matrix_frame.pack()

        self.add_red_button = tk.Button(self, text="Add Red Line", command=self.add_red_line)
        self.add_red_button.pack()

        self.add_blue_button = tk.Button(self, text="Add Blue Line", command=self.add_blue_line)
        self.add_blue_button.pack()

    def add_red_line(self):
        RedLine(self.matrix_frame).pack()

    def add_blue_line(self):
        BlueLine(self.matrix_frame).pack()


if __name__ == "__main__":
    app = MatrixApp()
    app.mainloop()
