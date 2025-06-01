import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import sys

def launch_game():
    subprocess.Popen([sys.executable, "2048.py"])

# Create main window
root = tk.Tk()
root.title("2048 Launcher")

# Make the window full screen or maximized
root.state('zoomed')  # For Windows, maximizes the window

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Load and resize background image to screen size
bg_image = Image.open("play.jpg").resize((screen_width, screen_height), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Set background image
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Optional: set icon
icon_img = Image.open("icon.jpg").resize((32, 32), Image.Resampling.LANCZOS)
icon_tk = ImageTk.PhotoImage(icon_img)
root.iconphoto(False, icon_tk)

# Transparent button over the "PLAY" area (based on new uploaded image)
# ⚠️ You may need to adjust x/y/width/height slightly depending on actual screen size and image scale
play_button = tk.Button(root, text="", command=launch_game, borderwidth=0, highlightthickness=0, bg=None, activebackground=None)
play_button.place(x=screen_width//2 - 110, y=screen_height//2 + 100, width=220, height=60)
play_button.lift()  # Bring to front

# Optional: change cursor on hover to indicate clickable area
play_button.config(cursor="hand2")

root.mainloop()
