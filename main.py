import customtkinter as ctk
from source.ui.mainui import ButtonRowApp


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
if __name__ == "__main__":
    root = ctk.CTk()
    app = ButtonRowApp(root)

    root.mainloop()