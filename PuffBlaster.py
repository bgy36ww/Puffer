from flask import Flask, request, render_template, redirect
from Controller import MainController
from Device import DeviceManager

app = Flask(__name__)
DATABASE = './data.db'
global controller
controller = None
global devices
devices = []
global pSuccess
pSuccess = 'successful'
global pList
pList = []


@app.route('/')
def hello_world():
    global controller
    global pList
    pList = controller.get_list()
    global devices
    devices = controller.get_devices()
    return render_template('main.html', pList=pList, devices=devices,
                           pSuccess=pSuccess)


@app.route('/run/url', methods=['post'])
def execute_url():
    global controller
    content = request.form['url']
    device = request.form['devices']
    test = request.form['tests']
    app_name = request.form['app']
    port = request.form['ports']
    if device:
        if test == 'hard cycle test':
            controller.run_cookie_task(device, port, app_name, content, True)
        elif test == 'soft cycle test':
            controller.run_cookie_task(device, port, app_name, content, False)
        elif test == 'Wake On Lan test':
            controller.run_wol_task(device, port, app_name, content, False)
        else:
            controller.run_url(device, app_name, content)
    print(content)
    print(device)
    return redirect('/')
# to do get json

@app.route('/process', methods=['post'])
def get_process():
    print("post called")
    print(request.form['name'])
    print(request.form.keys)
    global controller
    name = request.form['name']
    summary = str(controller.get_status(name))
    return summary

@app.route('/run/kill', methods=['post'])
def kill_process():
    global controller
    process = request.form['processes']
    controller.kill_process(process)
    return redirect('/')
# to do get json


def execute_task(device, port, app, content):
    global controller
    controller.run_cookie_task(device, port, app, content)


@app.route('/tasks', methods=['get'])
def get_tasks():
    pass
# to do get json


@app.route('/devices', methods=['get'])
def query_devices():
    global devices
    global controller
    global pSuccess
    controller.reconnect()
    devices = controller.devices
    pSuccess = 'successful' if controller.pSuccess \
        else 'not established'
    return redirect('/')


@app.route('/device/<device_id>', methods=['get'])
def query_device(device_id): pass


def setup_app(app):
    print('Connecting to a DLI PowerSwitch at lpc.digital-loggers.com')
    global controller
    controller = MainController()
    manager = DeviceManager(controller)
    manager.start()
    global pSuccess
    if not controller.pSuccess:
        pSuccess = 'not established'
    global pList
    pList = controller.get_list()


if __name__ == '__main__':
    setup_app(app)
    app.run(host='0.0.0.0')


