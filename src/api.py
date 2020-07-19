import time
from threading import Thread
from flask import Flask, jsonify
try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus
from bme280 import BME280
from sgp30 import SGP30

app = Flask(__name__)
smbus = SMBus(1)
bme280 = BME280(i2c_dev=smbus)
sgp30 = SGP30()
ready = False

def start_sgp30():
    sgp30.start_measurement()
    global ready
    ready = True
    while True:
        eco2, tvoc = sgp30.command('measure_air_quality')
        time.sleep(1)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/sensors', methods=['GET'])
def get_sensor_values():
    if not ready:
        return jsonify({"message": "sensors warming up"})
    temperature = round(bme280.get_temperature(), 2)
    humidity = round(bme280.get_humidity(), 2)
    pressure = round(bme280.get_pressure(), 2)
    eco2, tvoc = sgp30.command('measure_air_quality')
    json = {
        "temperature": temperature,
        "humidity": humidity,
        "pressure": pressure,
        "eco2": eco2,
        "tvoc": tvoc
    }
    return jsonify(json)


@app.route('/temperature', methods=['GET'])
def get_temperature():
    return str(bme280.get_temperature())


@app.route('/humidity', methods=['GET'])
def get_humidity():
    return str(bme280.get_humidity())


@app.route('/pressure', methods=['GET'])
def get_pressure():
    return str(bme280.get_pressure())


@app.route('/tvoc', methods=['GET'])
def get_tvoc():
    return str(tvoc)


@app.route('/eco2', methods=['GET'])
def get_eco2():
    return str(eco2)


@app.route('/cpu-temp', methods=['GET'])
def get_cpu_temp():
    return '0'


if __name__ == '__main__':
    t1 = Thread(target = start_sgp30)
    t1.setDaemon(True)
    t1.start()
    app.run(host='0.0.0.0', port=80)
