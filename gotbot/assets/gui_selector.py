import tkinter as tk
from tkinter import ttk
import json

CONFIG_PATH = "event_config.json"

def load_event_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def save_active_event(event_name):
    with open(CONFIG_PATH, "r+") as f:
        config = json.load(f)
        config["active_event"] = event_name
        f.seek(0)
        json.dump(config, f, indent=4)
        f.truncate()

def launch_event_selector():
    config = load_event_config()
    events = list(config["events"].keys())

    def on_select(event_name):
        save_active_event(event_name)
        print(f"Selected event: {event_name}")
        root.destroy()

    root = tk.Tk()
    root.title("Select Farming Event")
    root.geometry("300x150")

    label = ttk.Label(root, text="Choose an event to farm:")
    label.pack(pady=10)

    combo = ttk.Combobox(root, values=events, state="readonly")
    combo.set(config["active_event"])
    combo.pack(pady=5)

    button = ttk.Button(root, text="Confirm", command=lambda: on_select(combo.get()))
    button.pack(pady=10)

    root.mainloop()