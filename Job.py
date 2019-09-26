import time
import datetime
from Process import JobBase


class CookieJob(JobBase):
  def __init__(self, name, client, switch, port, duration, app,
      task, manager, power=True):
    super(JobBase, self).__init__(name, client, switch,
                                  port, duration, app, task, manager, power)

  def get_summary(self):
    summary = '\n Status: ' + self._status + '\n Loop count: ' + \
              str(self._loop_count)
    summary = summary + '\n DIAL error count: ' + str(self._error_count)
    summary = summary + '\n Time started: ' + datetime.datetime. \
      fromtimestamp(self._start).strftime('%Y-%m-%d %H:%M:%S')
    summary = summary + '\n Duration: ' + str(datetime.timedelta(
        seconds=time.time() - self._start))
    self._manager[self._name] = summary
    return summary

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
        print(e)

      try:
        time.sleep(200)
        if self.power:
          self.switch.off(self.port)
        self.check_paused()
      except Exception as e:
        self.error_count += 1
        print(e)
    self._status = 'finished'


class WolJob(JobBase):
  def __init__(self, name, client, switch, port, duration, app,
      task, manager, power=True):
    super(JobBase, self).__init__(name, client, switch,
                                  port, duration, app, task, manager, power)
    self.error_message = ''

  def get_summary(self):
    summary = '\n Status: ' + self._status
    summary = summary + '\n Time started: ' + datetime.datetime. \
      fromtimestamp(self._start).strftime('%Y-%m-%d %H:%M:%S')
    summary = summary + '\n Duration: ' + str(datetime.timedelta(
        seconds=time.time() - self._start))
    if self.error_message:
      summary = summary + '\n Errors: ' + self.error_message
    self._manager[self._name] = summary
    return summary

  def schedule(self):
    try:
      self.client.Close(self._app)
    except Exception as e:
      print('error closing app')
      print(e)
    self._status = 'running'
    try:
      self.client.Sleep()
      time.sleep(10)
      self.client.Wake()
      time.sleep(30)
      self.client.Sleep()
      time.sleep(25*60*60)
      self.client.Wake()
    except Exception as e:
      self.error_message = str(e)
      self._status = 'failed'