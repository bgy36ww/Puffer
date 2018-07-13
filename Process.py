import time
from multiprocessing import Process


class JobManager:
    def __init__(self, switch):
        self._pool = {}
        self._switch = switch

    def add(self, client, port, app, task):
        job = Job(client, self.switch, port, 200, app, task)
        job.start()
        self._pool[client] = job

    def pause(self, client):
        self._pool[client].pause()

    def resume(self, client):
        self._pool[client].resume()

    def get_status(self, client):
        return self._pool[client].get_status()

    def terminate(self, client):
        self._pool[client].terminate()

    def get_process(self, client):
        return self._pool[client]

    def is_alive(self, client):
        return self._pool[client].is_alive()


class Job(Process):
    def __init__(self, client, switch, port, loops, app, task):
        self.client = client
        self.switch = switch
        self.port = port
        self._operating = True
        self._loops = loops
        self._status = 'Created'
        self._paused = False
        self._app = app
        self._task = task

    def run(self):
        self.schedule()

    def get_status(self):
        return self._status

    def pause(self):
        self._paused = True

    def resume(self):
        self._paused = False

    def check_puased(self):
        while self._paused:
            pass

    def switch_task(self, app, task):
        self._app = app
        self._task = task

    def schedule(self):
        while self._operating and self._loops > 0:
            self._loops = self._loops-1
            self.switch.on(self.port)
            time.sleep(100)
            self.check_puased()
            res = self.client.Launch(self._app, self._task)
            res.raise_for_status()
            time.sleep(200)
            self.switch.off(self.port)
            self.check_puased()
