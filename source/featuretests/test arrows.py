import tkinter as tk

def update_digit_up(digit):
    current_value = int(canvas.itemcget(digit, "text"))
    new_value = (current_value + 1) % 10
    canvas.itemconfig(digit, text=str(new_value))

def update_digit_down(digit):
    current_value = int(canvas.itemcget(digit, "text"))
    new_value = (current_value - 1) % 10
    canvas.itemconfig(digit, text=str(new_value))

# Initialize the main window
root = tk.Tk()
root.title("Editable Clock")

# Create a Canvas widget for the clock display
canvas = tk.Canvas(root, width=300, height=100)
canvas.pack()

# Create text objects for each digit
digit1 = canvas.create_text(50, 50, text="0", font=("Helvetica", 36))
digit2 = canvas.create_text(100, 50, text="0", font=("Helvetica", 36))
colon = canvas.create_text(150, 50, text=":", font=("Helvetica", 36))
digit3 = canvas.create_text(200, 50, text="0", font=("Helvetica", 36))
digit4 = canvas.create_text(250, 50, text="0", font=("Helvetica", 36))

# Create up and down buttons for each digit
up1 = tk.Button(root, text="▲", command=lambda: update_digit_up(digit1))
down1 = tk.Button(root, text="▼", command=lambda: update_digit_down(digit1))
up2 = tk.Button(root, text="▲", command=lambda: update_digit_up(digit2))
down2 = tk.Button(root, text="▼", command=lambda: update_digit_down(digit2))
up3 = tk.Button(root, text="▲", command=lambda: update_digit_up(digit3))
down3 = tk.Button(root, text="▼", command=lambda: update_digit_down(digit3))
up4 = tk.Button(root, text="▲", command=lambda: update_digit_up(digit4))
down4 = tk.Button(root, text="▼", command=lambda: update_digit_down(digit4))

# Place the buttons on the canvas
canvas.create_window(50, 20, window=up1)
canvas.create_window(50, 80, window=down1)
canvas.create_window(100, 20, window=up2)
canvas.create_window(100, 80, window=down2)
canvas.create_window(200, 20, window=up3)
canvas.create_window(200, 80, window=down3)
canvas.create_window(250, 20, window=up4)
canvas.create_window(250, 80, window=down4)

# Run the tkinter main loop
root.mainloop()
