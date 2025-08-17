# Utility functions shared between bot.py and healing.py

def find_and_click(template_path, window_title="BlueStacks App Player", double=False):
    import pyautogui, cv2, pygetwindow as gw
    from PIL import ImageGrab
    import numpy as np
    import time
    import logging
    import os
    
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

    screen = capture_bluestacks_window(window_title)
    if screen is None:
        return False
    pos = find_button(screen, template_path)
    if pos:
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
        return True
    else:
        logging.warning(f"Button not found: {template_path}")
        return False

