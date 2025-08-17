import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'assets'))
# Imports
import os, time, json, logging
import pyautogui, cv2, pygetwindow as gw
from PIL import ImageGrab
import numpy as np
import keyboard
# from assets.gui_selector import launch_event_selector, load_event_config
from state import BotState
from healing import perform_healing
from utils import find_and_click

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("gotcbot.log"), logging.StreamHandler()]
)

# Pause toggle
paused = False
keyboard.add_hotkey('ctrl+shift+p', lambda: toggle_pause())

def toggle_pause():
    global paused
    paused = not paused
    logging.info(f"{'Paused' if paused else 'Resumed'} bot.")

# Window capture
def capture_bluestacks_window(window_title="BlueStacks App Player"):
    try:
        window = gw.getWindowsWithTitle(window_title)[0]
        if window.isMinimized or not window.visible:
            logging.warning("BlueStacks window is minimized or not visible.")
            return None
        left, top, right, bottom = window.left, window.top, window.right, window.bottom
        screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
        img_np = np.array(screenshot)
        return cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    except IndexError:
        logging.warning("BlueStacks window not found.")
        return None

# Template matching
def find_button(screen, template_path, threshold=0.04):
    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
    if template is None:
        logging.warning(f"Template not found: {template_path}")
        return None
    if template.shape[2] == 4:
        template = template[:, :, :3]
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    logging.info(f"Match confidence for {template_path}: {max_val:.2f}")
    if max_val >= threshold:
        h, w = template.shape[:2]
        return (max_loc[0] + w // 2, max_loc[1] + h // 2)
    return None

# Click logic
def click_at(pos, window_title="BlueStacks App Player", double=False):
    window = gw.getWindowsWithTitle(window_title)[0]
    x, y = pos
    click_x = window.left + x
    click_y = window.top + y
    pyautogui.moveTo(click_x, click_y)
    pyautogui.click()
    if double:
        time.sleep(0.3)
        pyautogui.click()
        time.sleep(0.2)
        pyautogui.moveTo(click_x, click_y - 90)
        time.sleep(1.5)
    logging.info(f"{'Double clicked' if double else 'Clicked'} at ({click_x}, {click_y})")



# Vision analysis
def analyze_screen(screen, assets_path):
    actions = {
        "ATTACK": "attack.png",
        "SEARCH": "search.png",
        "HEAL": "heal.png",
        "CREATURE_FOUND": "creature_found.png",
        "MARCH": "march.png"
    }
    for action, filename in actions.items():
        template_path = os.path.join(assets_path, filename)
        pos = find_button(screen, template_path)
        if pos:
            logging.info(f"[VISION] Detected {action} via {filename}")
            return action, pos
    return "IDLE", None

# Config loader
def load_config():
    with open("farming_config.json", "r") as f:
        return json.load(f)

# Main bot loop
def main():
    try:
        choice = int(input("Which farming mode?\n[1] Normal\n[2] Event\n> ").strip())
    except ValueError:
        logging.error("Invalid input. Please enter 1 or 2.")
        return

    if choice not in [1, 2]:
        logging.error("Invalid choice. Exiting.")
        return

    logging.info("Starting bot in 3 seconds...")
    time.sleep(3)

    config = load_config()
    assets = "assets/"
    bot_state = BotState()

    if choice == 2:
        from assets.gui_selector import launch_event_selector, load_event_config
        launch_event_selector()
        event_config = load_event_config()
        active_event = event_config["active_event"]
        event_data = event_config["events"][active_event]
        template_path = os.path.join(assets, event_data["template"])
        offset = event_data["click_offset"]

    while True:
        if paused:
            time.sleep(1)
            continue

        if bot_state.should_heal():
            bot_state.switch_state("HEALING")
            perform_healing(assets)
            bot_state.last_heal_time = time.time()
            bot_state.update_metrics("heals")
            bot_state.switch_state("FARMING")

        screen = capture_bluestacks_window()
        if screen is None:
            time.sleep(1)
            continue

        if choice == 1:
            pos = find_button(screen, template_path)
            if pos:
                x = pos[0] + offset[0]
                y = pos[1] + offset[1]
                click_at((x, y))
                bot_state.update_metrics("clicks")
                continue
            else:
                logging.warning(f"Event target not found: {active_event}")
                continue

        action, pos = analyze_screen(screen, assets)
        if action == "CREATURE_FOUND":
            click_at(pos, double=True)
            pyautogui.moveTo(pos[0], pos[1] - 90)
            bot_state.update_metrics("clicks")

# Entry point
if __name__ == "__main__":
    main()

       
