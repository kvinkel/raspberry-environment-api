import time
import threading
from flask import Flask, jsonify

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus
from bme280 import BME280
from sgp30 import SGP30
import database

app = Flask(__name__)
smbus = SMBus(1)
bme280 = BME280(i2c_dev=smbus)
lock = threading.Lock()
eco2, tvoc = 0, 0


# measure_air_quality command sent regularly for better baseline compensation
def start_sgp30(lock):
    sgp30 = SGP30()
    sgp30.start_measurement()
    global eco2, tvoc
    while True:
        with lock:
            eco2, tvoc = sgp30.command('measure_air_quality')
        time.sleep(1)


# First reading from bme will have lower readings if not used in a while
def discard_bme_reading():
    bme280.get_temperature()
    bme280.get_humidity()
    bme280.get_pressure()


def get_cpu_temp():
    file = open('/sys/class/thermal/thermal_zone0/temp')
    cpu_temp = file.readline().strip()
    file.close()
    return float(cpu_temp) / 1000


def start_data_save():
    time.sleep(60)  # Wait for sgp30 to warm up
    discard_bme_reading()
    while True:
        temp = round(bme280.get_temperature(), 2)
        hum = round(bme280.get_humidity(), 2)
        pres = round(bme280.get_pressure(), 2)
        cpu_temp = round(get_cpu_temp(), 2)
        with lock:
            t = tvoc
            e = eco2
        database.add_sensor_data(temp, hum, pres, t, e, cpu_temp)
        time.sleep(3600)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/sensors', methods=['GET'])
def get_sensor_values():
    discard_bme_reading()
    temperature = round(bme280.get_temperature(), 2)
    humidity = round(bme280.get_humidity(), 2)
    pressure = round(bme280.get_pressure(), 2)
    cpu_temp = round(get_cpu_temp(), 2)
    with lock:
        json = {
            "temperature": temperature,
            "humidity": humidity,
            "pressure": pressure,
            "eco2": eco2,
            "tvoc": tvoc,
            "cpu_temp": cpu_temp
        }
    return jsonify(json)


@app.route('/average', methods=['GET'])
def get_average():
    return jsonify(database.get_avg_data())


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
def get_cpu():
    return str(get_cpu_temp())


if __name__ == '__main__':
    database.set_up()
    t1 = threading.Thread(target=start_sgp30, args=(lock,))
    t1.setDaemon(True)
    t1.start()
    t2 = threading.Thread(target=start_data_save)
    t2.setDaemon(True)
    t2.start()
    app.run(host='0.0.0.0', port=80)
