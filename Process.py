import time
import datetime
from multiprocessing import Process, Manager


class JobManager:
    def __init__(self, switch):
        self._pool = {}
        self.switch = switch
        self.manager = Manager().dict()

    def add(self, name, client, port, app, task, power = True):
        if name in self._pool:
            self._pool[name].terminate()
        job = Job(name, client, self.switch, port, 86400, app, task, self.manager, power)
        self.manager[name] = job.get_summary()
        job.start()
        self._pool[name] = job

    def pause(self, name):
        self._pool[name].pause()

    def resume(self, name):
        self._pool[name].resume()

    def get_status(self, name):
        return self.manager[name]

    def terminate(self, name):
        self._pool[name].terminate()
        self._pool.pop(name)

    def get_process(self, name):
        return self._pool[name]

    def get_list(self):
        return self._pool.keys()

    def is_alive(self, name):
        return self._pool[name].is_alive()


class Job(Process):
    def __init__(self, name, client, switch, port, duration, app, task, manager, power = True):
        super(Job,self).__init__()
        self._name = name
        self._manager = manager
        self.client = client
        self.switch = switch
        self.port = port
        self._operating = True
        self._duration = duration
        self._status = 'Created'
        self._paused = False
        self._app = app
        self._task = task
        self.power = power
        self._start = time.time()
        self._loop_count = 0
        self._error_count = 0

    def run(self):
        self.schedule()

    def get_status(self):
        return self._status

    def pause(self):
        self._paused = True
        self._status = 'paused'

    def resume(self):
        self._paused = False
        self._status = 'running'

    def check_paused(self):
        while self._paused:
            pass

    def get_summary(self):
        summary = '\n Status: ' + self._status + '\n Loop count: ' + str(self._loop_count)
        summary = summary + '\n DIAL error count: ' + str(self._error_count)
        summary = summary + '\n Time started: ' + datetime.datetime.fromtimestamp(self._start).strftime('%Y-%m-%d %H:%M:%S')
        summary = summary + '\n Duration: ' + str(datetime.timedelta(seconds=time.time() - self._start))
        self._manager[self._name] = summary
        return summary

    def switch_task(self, app, task):
        self._app = app
        self._task = task

    def schedule(self):
        try:
            self.client.Close(self._app)
        except Exception as e:
            print('error closing app')
            print(e)
        self._status = 'running'
        while self._operating and time.time() - self._start < self._duration:
            try: 
                self._loop_count += 1
                print('loop starting')
                print(self._status)
                print(self.get_summary())
                self.switch.on(self.port)
                time.sleep(200)
                self.check_paused()
                res = self.client.Launch(self._app, self._task)
                res.raise_for_status()
            except Exception as e:
                self._error_count += 1
                print (e)

            try:
                time.sleep(200)
                if self.power:
                    self.switch.off(self.port)
                self.check_paused()
            except Exception as e:
                self.error_count += 1
                print(e)
        self._status = 'finished'

    def terminate(self):
        try:
            self.client.Close(self._app)
        except Exception as e:
            print('error closing app')
            print(e)
        super(Job,self).terminate()

