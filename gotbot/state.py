import time
import logging

class BotState:
    def __init__(self):
        self.state = "FARMING"
        self.last_heal_time = time.time()
        self.metrics = {
            "cycles": 0,
            "clicks": 0,
            "misses": 0,
            "heals": 0
        }

    def should_heal(self):
        return time.time() - self.last_heal_time >= 900  # 15 minutes

    def switch_state(self, new_state):
        logging.info(f"[STATE] Switching from {self.state} to {new_state}")
        self.state = new_state

    def update_metrics(self, key):
        if key in self.metrics:
            self.metrics[key] += 1

    def log_metrics(self):
        logging.info(f"[METRICS] {self.metrics}")