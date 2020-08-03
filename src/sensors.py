import time

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus
from bme280 import BME280
from sgp30 import SGP30

smbus = SMBus(1)
bme280 = BME280(i2c_dev=smbus)
sgp30 = SGP30()


def warmup_bar():
    print('#', end='', flush=True)


while True:
    user_input = input('Commands: bme280, sgp30, exit \n> ')
    if user_input == 'exit':
        quit()

    if user_input == 'bme280':
        for i in range(5):
            temperature = bme280.get_temperature()
            pressure = bme280.get_pressure()
            humidity = bme280.get_humidity()
            print('{:05.2f}*C {:05.2f}hPa {:05.2f}%'.format(temperature, pressure, humidity))
            time.sleep(1)

    if user_input == 'sgp30':
        print('Sensor warming up')
        sgp30.start_measurement(warmup_bar)
        for i in range(10):
            print(sgp30.get_air_quality())
            time.sleep(1)
