import time
import threading
from dial_client import util


class DeviceManager(threading.Thread):
    def __init__(self, controller):
        super(DeviceManager,self).__init__()
        self.controller = controller
        self.devices = []
        self._len = 0;
        self.device_map = {}

    def update_device_list(self):
        services = util.CaptureDevices()
        devices = []
        device_map = {}
        if len(services) != self._len:
            if self._len > len(services):
                print('device disconnected')
            else:
                print('new device added')
            self._len = len(services)
        for service in services:
            name = service.friendly_name
            device_map[name] = service
            devices.append(name)
        self.devices = devices
        self.device_map = device_map
        self.controller.update(device_map.copy(), devices.copy())

    def run(self):
        while True:
            try:
                time.sleep(0.5)
                self.update_device_list()
            except ConnectionError:
                print("Connection Error, Can't find Power Switch")
                print("Retry in 5 seconds")
                time.sleep(5)

