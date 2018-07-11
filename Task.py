import threading
import time


class Task (threading.Thread):
    def __init__(self, client, switch, port):
        self.client = client
        self.switch = switch
        self.port = port

    def run(self, app, task):
        self.switch.on(self.port)
        time.sleep(100)
        res = self.client.Launch(app, task)
        res.raise_for_status()
        time.sleep(200)
        self.switch.off(self.port) 
