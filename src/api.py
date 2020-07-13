from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/temperature', methods=['GET'])
def get_temperature():
    return 0


@app.route('/humidity', method=['GET'])
def get_humidity():
    return 0


@app.route('/pressure', method=['GET'])
def get_pressure():
    return 0


@app.route('/tvoc', method=['GET'])
def get_tvoc():
    return 0


@app.route('/eco2', method=['GET'])
def get_eco2():
    return 0


@app.route('cpu-temp', method=['GET'])
def get_cpu_temp():
    return 0


if __name__ == '__main__':
    app.run()
