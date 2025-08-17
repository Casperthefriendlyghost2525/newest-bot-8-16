import pyautogui
import pygetwindow as gw
from PIL import ImageGrab
import time
import json
from pynput import mouse
print("Script started")
WINDOW_TITLE = "BlueStacks App Player"

print("Move your mouse to the desired spot inside BlueStacks and LEFT CLICK to capture.")

def on_click(x, y, button, pressed):
    if pressed and button.name == 'left':
        window = gw.getWindowsWithTitle(WINDOW_TITLE)[0]
        rel_x = x - window.left
        rel_y = y - window.top
        bbox = (window.left, window.top, window.right, window.bottom)
        screenshot = ImageGrab.grab(bbox)
        screenshot.save("assets/captured_template.png")
        with open("assets/captured_coords.json", "w") as f:
            json.dump({"x": rel_x, "y": rel_y}, f)
        print(f"Captured at ({rel_x}, {rel_y}) and saved screenshot as 'assets/captured_template.png'.")
        return False  # Stop listener

with mouse.Listener(on_click=on_click) as listener:
    listener.join()