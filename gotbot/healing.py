import os
import time
import logging
from utils import find_and_click

def perform_healing(assets_path):
    logging.info("[*] Starting healing routine...")

    # Updated healing sequence with new template images:
    sequence = [
        "shield.png",         # 1st: find healing gear
        "healing_bar.png",   # 2nd: change to healing gear
        "helmet.png",        # 3rd: find troops to heal
        "herb.png",          # 4th: heal
        "heal.png"           # 5th: heal (button)
    ]

    for filename in sequence:
        full_path = os.path.join(assets_path, filename)
        for attempt in range(3):
            logging.info(f"[*] Healing step: {filename} (try {attempt + 1}/3)")
            if find_and_click(full_path):
                time.sleep(1)
                break
            time.sleep(2)
        else:
            logging.warning(f"[!] Failed to click {filename} during healing.")

    logging.info("[+] Healing complete.")