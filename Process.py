from multiprocessing import Manager, Process
import time
import datetime


class JobManager:
  def __init__(self, switch):
    self._pool = {}
    self.switch = switch
    self.manager = Manager().dict()

  def add(self, job, name):
    if name in self._pool:
      self._pool[name].terminate()
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


class JobBase(Process):
  def __init__(self, name, client, switch, port, duration, app,
      task, manager, power=True):
    super(JobBase, self).__init__()
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
    return ''

  def switch_task(self, app, task):
    self._app = app
    self._task = task

  def schedule(self):
    pass

  def terminate(self):
    try:
      self.client.Close(self._app)
    except Exception as e:
      print('error closing app')
      print(e)
    super(JobBase, self).terminate()
