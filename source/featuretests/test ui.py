import customtkinter as ctk
import source.ui.config as config

class MaterialDesignDemo(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Material Design Demo")
        self.geometry("400x600")
        self.configure(bg=config.COLOR_BACKGROUND)

        # Headline
        ctk.CTkLabel(self, text="Headline Text", font=config.FONT_HEADLINE, fg_color=config.COLOR_TEXT).pack(pady=config.SPACING_MEDIUM)

        # Title
        ctk.CTkLabel(self, text="Title Text", font=config.FONT_TITLE, fg_color=config.COLOR_TEXT).pack(pady=config.SPACING_MEDIUM)

        # Subtitle
        ctk.CTkLabel(self, text="Subtitle Text", font=config.FONT_SUBTITLE, fg_color=config.COLOR_TEXT_SECONDARY).pack(pady=config.SPACING_MEDIUM)

        # Body
        ctk.CTkLabel(self, text="Body Text", font=config.FONT_BODY, fg_color=config.COLOR_TEXT).pack(pady=config.SPACING_MEDIUM)

        # Button
        ctk.CTkButton(self, text="Button", font=config.FONT_BUTTON, fg_color=config.COLOR_PRIMARY, width=config.BUTTON_WIDTH, height=config.BUTTON_HEIGHT).pack(pady=config.SPACING_MEDIUM)

        # Entry
        ctk.CTkEntry(self, placeholder_text="Input Field", height=config.INPUT_HEIGHT).pack(pady=config.SPACING_MEDIUM)

        # Caption
        ctk.CTkLabel(self, text="Caption Text", font=config.FONT_CAPTION, fg_color=config.COLOR_TEXT_SECONDARY).pack(pady=config.SPACING_MEDIUM)

if __name__ == "__main__":
    app = MaterialDesignDemo()
    app.mainloop()