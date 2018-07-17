from multiprocessing import Process
import time
from dial_client import util


class DeviceManager(Process):
    def __init__(self, controller):
        self.controller = controller
        self.devices = []

    def update_device_list(self):
        print('finding devices')
        services = util.CaptureDevices()
        devices = []
        device_map = {}
        if len(services) == 0:
            print('no device is available')
        for service in services:
            name = service.friendly_name
            device_map[name] = service
            devices.append(name)
        self.controller.update(device_map, devices)

    def run(self):
        while True:
            try:
                time.sleep(0.5)
                self.update_device_list()
            except ConnectionError:
                print("Connection Error, Can't find Power Switch")
                print("Retry in 5 seconds")
                time.sleep(5)

