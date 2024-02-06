import threading
import time
class EmailThreading(threading.Thread):
    def __init__(self, Email):
        super().__init__()
        time.sleep(5)
        self.Email = Email

    def run(self) -> None:

        self.Email.send()
