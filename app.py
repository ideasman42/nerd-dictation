# This GUI app requires an image called icon.png to be used as the icon for the app
# so make sure to have one in the same folder as this file, or it will crash.
# If you don't really care, you can just comment out all references to icons
# Also, it is recommended to turn this file into an executable using pyinstaller, as it makes the whole experience much smoother

import tkinter as tk
from tkinter import messagebox
import subprocess
import os

# --- Configuration ---
BASE_PROJECT_DIR = "/home/james/Desktop/Projects/nerd-dictation"
VENV_PYTHON_PATH = os.path.join(BASE_PROJECT_DIR, ".venv/bin/python")
NERD_DICTATION_SCRIPT_PATH = os.path.join(BASE_PROJECT_DIR, "nerd-dictation")
MODEL_DIR_RELATIVE = "./model"
ICON_FILE_NAME = "icon.png" 

START_COMMAND_STR = f"{VENV_PYTHON_PATH} {NERD_DICTATION_SCRIPT_PATH} begin --vosk-model-dir={MODEL_DIR_RELATIVE} &"
STOP_COMMAND_ARGS = [VENV_PYTHON_PATH, NERD_DICTATION_SCRIPT_PATH, "end"]
WORKING_DIRECTORY = BASE_PROJECT_DIR

# --- Global State ---
nerd_dictation_process = None
is_running = False

# --- Functions ---
def start_nerd_dictation():
    global is_running, nerd_dictation_process

    if is_running:
        print("Nerd Dictation is already running.")
        return

    try:
        print(f"Attempting to start Nerd Dictation...")
        print(f"Command: {START_COMMAND_STR}")
        print(f"Working Directory: {WORKING_DIRECTORY}")

        nerd_dictation_process = subprocess.Popen(
            START_COMMAND_STR,
            shell=True,
            cwd=WORKING_DIRECTORY,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(f"Nerd Dictation process started (PID: {nerd_dictation_process.pid if nerd_dictation_process else 'Unknown'}).")
        is_running = True
        start_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)
        status_label.config(text="Status: Running", fg="green")
    except Exception as e:
        messagebox.showerror("Error Starting", f"Failed to start Nerd Dictation:\n{e}")
        status_label.config(text=f"Status: Error starting", fg="red")
        print(f"Error starting Nerd Dictation: {e}")

def stop_nerd_dictation():
    global is_running, nerd_dictation_process

    try:
        print(f"Attempting to stop Nerd Dictation...")
        print(f"Command: {' '.join(STOP_COMMAND_ARGS)}")
        print(f"Working Directory: {WORKING_DIRECTORY}")

        stop_process = subprocess.Popen(
            STOP_COMMAND_ARGS,
            cwd=WORKING_DIRECTORY,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = stop_process.communicate(timeout=10)
        
        if stop_process.returncode == 0:
            print("Nerd Dictation 'end' command executed successfully.")
        else:
            print(f"Nerd Dictation 'end' command finished with code {stop_process.returncode}.")
            print(f"STDOUT: {stdout.decode() if stdout else 'None'}")
            print(f"STDERR: {stderr.decode() if stderr else 'None'}")

        is_running = False
        start_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)
        status_label.config(text="Status: Stopped", fg="black")
        nerd_dictation_process = None

    except subprocess.TimeoutExpired:
        messagebox.showwarning("Timeout", "The 'nerd-dictation end' command timed out.")
        status_label.config(text="Status: Stop timed out", fg="orange")
        is_running = False
        start_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)
        nerd_dictation_process = None
        print("Timeout while waiting for Nerd Dictation to stop.")

    except Exception as e:
        messagebox.showerror("Error Stopping", f"Failed to stop Nerd Dictation:\n{e}")
        status_label.config(text=f"Status: Error stopping", fg="red")
        print(f"Error stopping Nerd Dictation: {e}")


def on_closing():
    if is_running:
        if messagebox.askyesno("Quit", "Nerd Dictation is running. Do you want to stop it before quitting?"):
            stop_nerd_dictation()
            if not is_running:
                root.destroy()
        else:
            root.destroy()
    else:
        root.destroy()

# --- GUI Setup ---
root = tk.Tk()
root.title("Nerd Dictation Controller")

# --- Set the window icon ---
try:
    # Get the directory where the script is running
    script_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(script_dir, ICON_FILE_NAME)

    if os.path.exists(icon_path):
        # The 'True' argument tells Tkinter to use this as the default icon.
        # Tkinter's PhotoImage can handle PNG, GIF, PPM/PGM.
        img = tk.PhotoImage(file=icon_path)
        root.iconphoto(True, img)
    else:
        print(f"Icon file not found: {icon_path}")
except tk.TclError as e:
    # This can happen if the image format is not supported or file is corrupt
    print(f"Error loading icon '{ICON_FILE_NAME}': {e}")
    print("Make sure 'icon.png' is a valid PNG/GIF image and Pillow is installed if needed ('pip install Pillow').")
except Exception as e:
    print(f"An unexpected error occurred while setting the icon: {e}")


root.geometry("300x200")

button_frame = tk.Frame(root)
button_frame.pack(pady=20)

start_button = tk.Button(
    button_frame,
    text="START",
    command=start_nerd_dictation,
    width=12,
    height=2,
    font=("Arial", 12),
    bg="green",
    fg="white"
)
start_button.pack(side=tk.LEFT, padx=10)

stop_button = tk.Button(
    button_frame,
    text="STOP",
    command=stop_nerd_dictation,
    width=12,
    height=2,
    font=("Arial", 12),
    state=tk.DISABLED,
    bg="red",
    fg="white"
)
stop_button.pack(side=tk.LEFT, padx=10)

status_label = tk.Label(root, text="Status: Stopped", font=("Arial", 10), fg="black")
status_label.pack(pady=10)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()