import time
import threading
from flask import Flask, jsonify
import database
import math

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus
from bme280 import BME280
from sgp30 import SGP30

app = Flask(__name__)
smbus = SMBus(1)
bme280 = BME280(i2c_dev=smbus)
lock = threading.Lock()
eco2, tvoc = 0, 0


# Formula source: https://carnotcycle.wordpress.com/2012/08/04/how-to-convert-relative-humidity-to-absolute-humidity/
# Accurate to within 0.1% over the temperature range –30°C to +35°C
def calculate_absolute_humidity(temp, relative_hum):
    return (6.112 * pow(math.e, (17.67 * temp) / (temp + 243.5)) * relative_hum * 2.1674) / (273.15 + temp)  # g/m³


# measure_air_quality command sent regularly for better baseline compensation
def start_sgp30(lock):
    sgp30 = SGP30()
    sgp30.start_measurement()
    global eco2, tvoc
    while True:
        with lock:
            eco2, tvoc = sgp30.command('measure_air_quality')
        time.sleep(1)


def get_cpu_temp():
    file = open('/sys/class/thermal/thermal_zone0/temp')
    cpu_temp = file.readline().strip()
    file.close()
    return float(cpu_temp) / 1000


def start_data_save():
    time.sleep(60)  # Wait for sgp30 to warm up
    sgp = SGP30()
    while True:
        temp = bme280.get_temperature()
        hum = bme280.get_humidity()
        pres = bme280.get_pressure()
        cpu_temp = get_cpu_temp()
        with lock:
            t = tvoc
            e = eco2
        database.add_sensor_data(temp, hum, pres, t, e, cpu_temp)
        time.sleep(3600)
        eco2_base, tvoc_base = sgp.command('get_baseline')
        database.set_baseline(eco2_base, tvoc_base)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/sensors', methods=['GET'])
def get_sensor_values():
    temperature = bme280.get_temperature()
    humidity = bme280.get_humidity()
    pressure = bme280.get_pressure()
    cpu_temp = get_cpu_temp()
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


@app.route('/min_max', methods=['GET'])
def get_min_max():
    return jsonify(database.get_min_max())


@app.route('/measurement_info', methods=['GET'])
def get_measurement_info():
    return jsonify(database.get_measurement_info())


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


def set_sgp30_baseline():
    sg = SGP30()
    eco2_base, tvoc_base = database.get_baseline()
    if eco2_base != 0:
        sg.command('set_baseline', (eco2_base, tvoc_base))


if __name__ == '__main__':
    # First reading from bme is inaccurate
    bme280.get_temperature()
    bme280.get_humidity()
    bme280.get_pressure()
    database.set_up()
    set_sgp30_baseline()
    t1 = threading.Thread(target=start_sgp30, args=(lock,))
    t1.setDaemon(True)
    t1.start()
    t2 = threading.Thread(target=start_data_save)
    t2.setDaemon(True)
    t2.start()
    app.run(host='0.0.0.0', port=80)
