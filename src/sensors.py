import time

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus
from bme280 import BME280

smbus = SMBus(1)
bme280 = BME280(i2c_dev=smbus)

while True:
    user_input = input('Commands: bme, exit \n> ')
    if user_input == 'exit':
        quit()

    if user_input == 'bme':
        for i in range(5):
            temperature = bme280.get_temperature()
            pressure = bme280.get_pressure()
            humidity = bme280.get_humidity()
            print('{:05.2f}*C {:05.2f}hPa {:05.2f}%'.format(temperature, pressure, humidity))
            time.sleep(1)
