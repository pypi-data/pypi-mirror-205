import keyboard
import threading


class GlobalKeyBoard:
    def __init__(self):
        self.hotkeys = {}

    def add(self, hot_key, func):
        self.hotkeys[hot_key] = func

    def run(self):
        def run_threading(*args):
            for key in self.hotkeys:
                keyboard.add_hotkey(key, self.hotkeys[key])
            keyboard.wait()

        threading.Thread(target=run_threading).start()
