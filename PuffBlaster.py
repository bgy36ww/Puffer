from flask import Flask, request, render_template, redirect
import time
from dial_client import util
from Controller import MainController
import sqlite3
from flask import g

app = Flask(__name__)
DATABASE = './data.db'


@app.route('/')
def hello_world():
    return render_template('main.html', devices=devices,
                           pSuccess=pSuccess)


@app.route('/run/url', methods=['post'])
def execute_url():
    content = request.form['url']
    device = request.form['devices']
    test = request.form['tests']
    app = request.form['app']
    port = request.form['ports']
    switch.on(port)
    if device:
        deviceMap[device].Close(app)
        if test == 'test':
            execute_task(device, port, app, content)
        else:
            deviceMap[device].Launch(app, content)
    print(content)
    print(device)
    return redirect('/')
# to do get json


def execute_task(device, port, app, content):
    retry=40000
    powerRetry = 0
    global switch
    while retry>0:
        try:
            retry = retry - 1
            service = deviceMap[device]
            service.GetApp(app)
            service.Close(app)
            task = Task(service, switch, port)
            task.run(app, content)
        except Exception as e:
            print(e)
            switch.on(port)
            if powerRetry%10 == 0:
                switch.off(port)
                switch.on(port)
            time.sleep(20)
            update_device_list() 
    pass


@app.route('/tasks', methods=['get'])
def get_tasks():
    pass
# to do get json


@app.route('/devices', methods=['get'])
def query_devices():
    global devices
    update_device_list()
    global pSuccess
    if not pSuccess:
        try:
            switch.verify()
        except:
            pSuccess = 'failed'
    return redirect('/')


@app.route('/device/<device_id>', methods=['get'])
def query_device(device_id): pass


def get_db():
    db = getattr(g, '_database', None)


def update_device_list():
    print('finding devices')
    global devices
    global deviceMap
    services = util.CaptureDevices()
    devices = []
    if len(services) == 0:
        print('no device is available')
    for service in services:
        name = service.friendly_name
        deviceMap[name] = service
        devices.append(name)


def setup_app(app):
    print('Connecting to a DLI PowerSwitch at lpc.digital-loggers.com')
    controller = MainController()


if __name__ == '__main__':
    setup_app(app)
    app.run(host='0.0.0.0')


