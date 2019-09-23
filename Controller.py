from Process import JobManager
import dlipower


class MainController:
    def __init__(self):
        self.pSuccess = False
        self._switch = dlipower.PowerSwitch(hostname="192.168.0.100",
                                            userid="admin", password='1234')
        self.pSuccess = self._switch.verify()
        for i in range(1, 8):
            self._switch.off(i)
            self._switch.on(i)
        self.jobManager = JobManager(self._switch)
        self.device_map = {}
        self.devices = []

    def update(self, device_map, devices):
        self.device_map = device_map
        self.devices = devices

    def run_url(self, name, url, content):
        self.device_map[name].Launch(url, content)

    def run_task(self, name, port, app, task, power = True):
        client = self.device_map[name]
        self.jobManager.add(name, client, port, app, task, power)

    def query_devices(self):
        return self.device_map

    def reconnect(self):
        self.pSuccess = self._switch.verify()

    def get_list(self):
        return self.jobManager.get_list()

    def kill_process(self, name):
        self.jobManager.terminate(name)

    def get_status(self, name):
        return self.jobManager.get_status(name)

    def get_devices(self):
        return self.devices

