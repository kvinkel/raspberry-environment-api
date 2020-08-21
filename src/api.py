import time
import threading
import database
import math
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus
from bme280 import BME280
from sgp30 import SGP30

app = FastAPI()
smbus = SMBus(1)
bme280 = BME280(i2c_dev=smbus)
lock = threading.Lock()
eco2, tvoc = 0, 0


def get_cpu_temp():
    file = open('/sys/class/thermal/thermal_zone0/temp')
    cpu_temp = file.readline().strip()
    file.close()
    return float(cpu_temp) / 1000


# Formula source: https://carnotcycle.wordpress.com/2012/08/04/how-to-convert-relative-humidity-to-absolute-humidity/
# Within 0.1% accuracy over temperature range –30°C to +35°C
def calculate_absolute_humidity(temp, relative_hum):
    return (6.112 * pow(math.e, (17.67 * temp) / (temp + 243.5)) * relative_hum * 2.1674) / (273.15 + temp)  # g/m³


# Humidity compensation info: SGP30 datasheet page 8/15
def convert_absolute_humidity(absolute_hum):
    aft_dec, bef_dec = math.modf(absolute_hum)
    bef = int(bef_dec)
    aft = round(aft_dec * 256)
    if bef > 255:
        return 0
    if aft > 255:
        aft = 255
    hum_hex = '0x{:02X}'.format(bef) + '{:02X}'.format(aft)
    return int(hum_hex, 0)


# measure_air_quality command sent regularly for better baseline compensation
def start_sgp30(lock):
    sgp30 = SGP30()
    sgp30.start_measurement()
    global eco2, tvoc
    counter = 0
    while True:
        with lock:
            eco2, tvoc = sgp30.command('measure_air_quality')
        counter += 1
        if counter == 600:
            counter = 0
            absolute_hum = calculate_absolute_humidity(bme280.get_temperature(), bme280.get_humidity())
            sgp30.command('set_humidity', (convert_absolute_humidity(absolute_hum),))
        time.sleep(1)


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


@app.get('/', response_class=PlainTextResponse)
def hello_world():
    return 'Hello World!'


@app.get('/sensors')
def get_sensor_values():
    temperature = bme280.get_temperature()
    humidity = bme280.get_humidity()
    pressure = bme280.get_pressure()
    cpu_temp = get_cpu_temp()
    with lock:
        sensor_values = {
            "temperature": temperature,
            "humidity": humidity,
            "pressure": pressure,
            "eco2": eco2,
            "tvoc": tvoc,
            "cpu_temp": cpu_temp
        }
    return sensor_values


@app.get('/average')
def get_average():
    return database.get_avg_data()


@app.get('/min_max')
def get_min_max():
    return database.get_min_max()


@app.get('/measurement_info')
def get_measurement_info():
    return database.get_measurement_info()


@app.get('/temperature', response_class=PlainTextResponse)
def get_temperature():
    return str(bme280.get_temperature())


@app.get('/humidity', response_class=PlainTextResponse)
def get_humidity():
    return str(bme280.get_humidity())


@app.get('/pressure', response_class=PlainTextResponse)
def get_pressure():
    return str(bme280.get_pressure())


@app.get('/tvoc', response_class=PlainTextResponse)
def get_tvoc():
    return str(tvoc)


@app.get('/eco2', response_class=PlainTextResponse)
def get_eco2():
    return str(eco2)


@app.get('/cpu-temp', response_class=PlainTextResponse)
def get_cpu():
    return str(get_cpu_temp())


def set_sgp30_baseline():
    sg = SGP30()
    eco2_base, tvoc_base = database.get_baseline()
    if eco2_base != 0:
        sg.command('set_baseline', (eco2_base, tvoc_base))


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
