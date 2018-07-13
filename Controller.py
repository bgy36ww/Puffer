from Process import JobManager
from Device import DeviceManager
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
        self.deviceManager = DeviceManager(self)
        self.deviceManager.start()
        self.device_map = {}

    def update(self, device_map):
        self.device_map = device_map

    def run_url(self, url, index): pass

    def run_task(self): pass

    def query_devices(self): pass

