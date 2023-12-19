import tkinter as tk
import customtkinter as ctk
import time

title_bar_height = 30  #Global variable, 30 pixels for the window title bar in tkinter

class ToastNotification:
    def __init__(self, root, message):
        """Construct a toast.

        root, the window the toast needs to appear ontop.
        message, the message required to display.

        If NAME matches an existing variable and VALUE is omitted
        then the existing value is retained.
        """
        self.root = root
        self.message = message
        self.toast_window = None
        self.duration = 3  # Duration in seconds

    def show(self):
        if self.toast_window is not None:
            self.toast_window.destroy()

        main_window_x = self.root.winfo_x()
        main_window_y = self.root.winfo_y()
        main_window_width = self.root.winfo_width()
        main_window_height = self.root.winfo_height()

        label = ctk.CTkLabel(self.root, text=self.message)
        label.update_idletasks()  # Update the label to get its actual width
        text_width = label.winfo_reqwidth()

        toast_width = text_width + 20  # Add padding for aesthetics
        toast_height = 30
        distance_from_bottom = 12

        print(main_window_x, main_window_width, toast_width)
        x = main_window_x + (main_window_width - toast_width) // 2
        y = main_window_y + main_window_height + title_bar_height - toast_height - distance_from_bottom
        print(x)
        self.toast_window = ctk.CTkToplevel(self.root)
        self.toast_window.overrideredirect(True)  # Remove window decorations
        self.toast_window.geometry("{}x{}+{}+{}".format(toast_width, toast_height, x, y))
        self.toast_window.configure(bg="black")

        label = ctk.CTkLabel(
            self.toast_window,
            bg_color="black",
            text=self.message,
            padx=10,
            pady=5
        )
        label.pack(fill="both", expand=True)

        self.root.after(int(self.duration * 1000), self.close)

    def close(self):
        if self.toast_window is not None:
            self.toast_window.destroy()
            self.toast_window = None


def show_toast(root, message):
    toast = ToastNotification(root, message)
    toast.show()


#"""
if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("400x200")
    root.title("Toast Notification Example")

    button = ctk.CTkButton(root, text="Show Toast", command=lambda: show_toast(root, "This is a centered toast notification with dynamic width."))
    button.pack(pady=20)

    root.mainloop()

fg = "white",
bg = "black",
#"""