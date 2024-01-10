import tkinter as tk

def create_color_display_with_buttons_app():
    # Color scheme
    colors = {
        "Primary Color (#2979FF)": "#1B4242",
        "Primary Variant (#1565C0)": "#286464",
        "Secondary Color (#03DAC6)": "#468282",
        "Background (#121212)": "#242424",
        "Surface (#1E1E1E)": "#1E1E1E",
        "Error (#CF6679)": "#CF6679",
        "On Primary (#FFFFFF)": "#FFFFFF",
        "On Secondary (#FFFFFF)": "#FFFFFF",
        "On Background (#E0E0E0)": "#242424",
        "On Surface (#E0E0E0)": "#E0E0E0"
    }

    # Create the main window
    root = tk.Tk()
    root.title("Color Scheme Display with Buttons")
    root.geometry("400x700")
    root.configure(bg=colors["Background (#121212)"])

    # Function to create a colored frame with a label
    def create_colored_frame(container, color_name, hex_code):
        frame = tk.Frame(container, height=50, bg=hex_code)
        frame.pack(padx=10, pady=5, fill="x")
        label = tk.Label(frame, text=color_name, bg=hex_code, fg="#FFFFFF")
        label.pack(side="left", padx=10)

    # Create a frame for each color in the color scheme
    for color_name, hex_code in colors.items():
        create_colored_frame(root, color_name, hex_code)

    # Adding buttons with appropriate colors
    button_frame = tk.Frame(root, bg=colors["Surface (#1E1E1E)"])
    button_frame.pack(padx=10, pady=10, fill="x")

    # Buttons
    tk.Button(button_frame, text="Load", bg=colors["Primary Color (#2979FF)"], fg=colors["On Primary (#FFFFFF)"]).pack(side="left", padx=5, pady=5)
    tk.Button(button_frame, text="Save", bg=colors["Secondary Color (#03DAC6)"], fg=colors["On Secondary (#FFFFFF)"]).pack(side="left", padx=5, pady=5)
    tk.Button(button_frame, text="Cancel", bg=colors["Error (#CF6679)"], fg=colors["On Primary (#FFFFFF)"]).pack(side="left", padx=5, pady=5)
    tk.Button(button_frame, text="Quit", bg=colors["Primary Variant (#1565C0)"], fg=colors["On Primary (#FFFFFF)"], command=root.destroy).pack(side="left", padx=5, pady=5)

    # Run the application
    root.mainloop()

# Run this script in a Python environment with tkinter installed to view the color scheme with buttons.
create_color_display_with_buttons_app()
"""
dark Green color selection
"Primary Color (#2979FF)": "#1B4242",
"Primary Variant (#1565C0)": "#286464",
"Secondary Color (#03DAC6)": "#468282",



general selection
        "Primary Color (#2979FF)": "#091540",
        "Primary Variant (#1565C0)": "#1565C0",
        "Secondary Color (#03DAC6)": "#03DAC6",
        
        
        
        
        colors = {
        "Primary Color (#2979FF)": "#1B4242",
        "Primary Variant (#1565C0)": "#286464",
        "Secondary Color (#03DAC6)": "#468282",
        "Background (#121212)": "#242424",
        "Surface (#1E1E1E)": "#1E1E1E",
        "Error (#CF6679)": "#CF6679",
        "On Primary (#FFFFFF)": "#FFFFFF",
        "On Secondary (#FFFFFF)": "#FFFFFF",
        "On Background (#E0E0E0)": "#E0E0E0",
        "On Surface (#E0E0E0)": "#E0E0E0"
    }
"""