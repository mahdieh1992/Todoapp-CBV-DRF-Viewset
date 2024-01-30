import threading


class EmailThreading(threading.Thread):
    def __init__(self, Email):
        super().__init__()
        self.Email = Email

    def run(self) -> None:
        self.Email.send()
