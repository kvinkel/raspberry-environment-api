from flask import Flask, jsonify
try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus
from bme280 import BME280

app = Flask(__name__)
smbus = SMBus(1)
bme280 = BME280(i2c_dev=smbus)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/sensors')
def get_sensor_values():
    temperature = round(bme280.get_temperature(), 2)
    humidity = round(bme280.get_humidity, 2)
    pressure = round(bme280.get_pressure, 2)
    json = {
        "temperature": temperature,
        "humidity": humidity,
        "pressure": pressure
    }
    return jsonify(json)


@app.route('/temperature', methods=['GET'])
def get_temperature():
    return bme280.get_temperature()


@app.route('/humidity', method=['GET'])
def get_humidity():
    return bme280.get_humidity()


@app.route('/pressure', method=['GET'])
def get_pressure():
    return bme280.get_pressure()


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
