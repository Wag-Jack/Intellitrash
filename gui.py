import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from playsound import playsound
import random

# Function to update the trashcan's status
def update_trashcan_status():
    global progress, canvas_img

    #jack pls change
    distance = random.uniform(5, 20)  
    max_distance = 20  
    progress = max(0, min(100, 100 - (distance / max_distance) * 100))

    # Update progress bar
    progress_bar["value"] = progress

    # Update the status summary
    if progress < 50:
        status_summary.config(text=f"Trashcan is {int(progress)}% Full", fg="green")
        img = ImageTk.PhotoImage(Image.open("trashcan_green.png"))
    elif progress < 90:
        status_summary.config(text=f"Trashcan is {int(progress)}% Full", fg="orange")
        img = ImageTk.PhotoImage(Image.open("trashcan_yellow.png"))
    else:
        status_summary.config(text=f"Trashcan is {int(progress)}% Full", fg="red")
        img = ImageTk.PhotoImage(Image.open("trashcan_red.png"))
        if progress == 100:
            alert_user("Trashcan is Full!")

    # Update the trashcan image
    canvas.itemconfig(canvas_img, image=img)
    canvas.image = img  
    
# Function to alert the user
def alert_user(message):
    messagebox.showwarning("Trashcan Full Alert", message)
    status_summary.config(text=message, fg="red")

# Function to reset the trashcan status
def reset_trashcan_status():
    progress_bar["value"] = 0
    status_summary.config(text="Trashcan is Empty", fg="green")
    img = ImageTk.PhotoImage(Image.open("trashcan_green.png"))
    canvas.itemconfig(canvas_img, image=img)
    canvas.image = img  # Keep a reference

# Set up the main GUI window
root = tk.Tk()
root.title("IntelliTrash")
root.geometry("400x500")

# Top Section: Title and Status Summary
title = tk.Label(root, text="IntelliTrash", font=("Arial", 20, "bold"))
title.pack(pady=10)

status_summary = tk.Label(root, text="Trashcan is Empty", font=("Arial", 14), fg="green")
status_summary.pack(pady=5)

# Middle Section: Trashcan Image and Progress Bar
canvas = tk.Canvas(root, width=200, height=200)
canvas.pack(pady=20)

img = ImageTk.PhotoImage(Image.open("trashcan_green.png"))  # Initial empty trashcan image
canvas_img = canvas.create_image(100, 100, anchor=tk.CENTER, image=img)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=10)

# Bottom Section: Refresh/Reset Button
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

refresh_button = tk.Button(button_frame, text="Refresh", font=("Arial", 12), command=update_trashcan_status)
refresh_button.grid(row=0, column=0, padx=10)

reset_button = tk.Button(button_frame, text="Reset", font=("Arial", 12), command=reset_trashcan_status)
reset_button.grid(row=0, column=1, padx=10)

# Simulate status updates every 5 seconds
def simulate_updates():
    update_trashcan_status()
    root.after(5000, simulate_updates)

simulate_updates()

# Start the GUI loop
root.mainloop()
