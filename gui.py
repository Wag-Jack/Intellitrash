import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# Global state dictionary for GUI references
state = {}

# Function to update the trashcan's status
def update_trashcan_status(status_bounds, status_flag, sensor_reading, trash_height):
    global state

    #Converts sensor data to be received by the GUI
    distance = sensor_reading 
    max_distance = trash_height
    progress = max(0, min(100, 100 - (distance / max_distance) * 100))

    # Update progress bar
    state['progress_bar']["value"] = progress

    """
    TODO: Fix issue with trash only being scanned as red here
    """

    # Update the status summary
    status_summary = state['status_summary']
    if status_flag == 'RED': #Trashcan close to full
        status_summary.config(text=f'Trashcan is {int(progress)}% Full', fg='red')
        img = ImageTk.PhotoImage(Image.open('trashcan_red.png'))
        if progress == 100: #Trashcan is full
            alert_user('Trashcan is full!')
    elif status_flag == 'YELLOW': #Trashcan in yellow zone
        status_summary.config(text=f'Trashcan is {int(progress)}% Full', fg='orange')
        img = ImageTk.PhotoImage(Image.open('trashcan_yellow.png'))
    elif status_flag == 'GREEN': #Trashcan in green zone
        status_summary.config(text=f'Trashcan is {int(progress)}% Full', fg='green')
        img = ImageTk.PhotoImage(Image.open('trashcan_green.png'))
    else: #Trashcan is open
        status_summary.config(text='Trashcan open! Please close!', fg='green')
        img = ImageTk.PhotoImage(Image.open('trashcan_green.png'))

    # Update the trashcan image
    canvas = state['canvas']
    canvas.itemconfig(state['canvas_img'], image=img)
    canvas.image = img  
    
# Function to alert the user
def alert_user(message):
    global state
    status_summary = state['status_summary']
    messagebox.showwarning("Trashcan Full Alert", message)
    status_summary.config(text=message, fg="red")

# Function to reset the trashcan status
def reset_trashcan_status():
    global state

    state['progress_bar']["value"] = 0
    state['status_summary'].config(text="Trashcan is Empty", fg="green")
    img = ImageTk.PhotoImage(Image.open("trashcan_green.png"))
    
    canvas = state['canvas']
    canvas.itemconfig(state['canvas_img'], image=img)
    canvas.image = img  # Keep a reference

def initialize_gui(root):
    global state

    # Set up the main GUI window
    root.title("IntelliTrash")
    root.geometry("400x500")

    # Top Section: Title and Status Summary
    title = tk.Label(root, text="IntelliTrash", font=("Arial", 20, "bold"))
    title.pack(pady=10)

    status_summary = tk.Label(root, text="Trashcan is Empty", font=("Arial", 14), fg="green")
    status_summary.pack(pady=5)
    state['status_summary'] = status_summary

    # Middle Section: Trashcan Image and Progress Bar
    canvas = tk.Canvas(root, width=200, height=200)
    canvas.pack(pady=20)
    state['canvas'] = canvas

    img = ImageTk.PhotoImage(Image.open("trashcan_green.png"))  # Initial empty trashcan image
    canvas_img = canvas.create_image(100, 100, anchor=tk.CENTER, image=img)
    state['canvas_img'] = canvas_img

    progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=10)
    state['progress_bar'] = progress_bar

    # Bottom Section: Refresh/Reset Button
    button_frame = tk.Frame(root)
    button_frame.pack(pady=20)

    refresh_button = tk.Button(button_frame, text="Refresh", font=("Arial", 12), command=update_trashcan_status)
    refresh_button.grid(row=0, column=0, padx=10)

    reset_button = tk.Button(button_frame, text="Reset", font=("Arial", 12), command=reset_trashcan_status)
    reset_button.grid(row=0, column=1, padx=10)

    return state