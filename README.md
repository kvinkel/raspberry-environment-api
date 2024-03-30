# Raspberry Environment aPi

API for monitoring local environment temperature, humidity, pressure, TVOC, and eCO2 on a Raspberry Pi. The sensors used are the BME280 Sensor Breakout and the SGP30 Air Quality Sensor Breakout from Pimoroni. The project aims to provide easy access to current air quality readings and an overview of past readings and tendencies using Python, SQLite, and Docker.

## Endpoints

`/`

Links and descriptions of the different endpoints

`/sensors`

Readings from the sensors: temperature in degrees Celsius (°C), relative humidity percentage (%), pressure in hectopascal pressure units (hPa), CO2 in parts-per million from 400-60,000 (ppm), total volatile organic compounds in parts-per billion 0-60,000 (TVOC in ppb), and CPU temperature in degrees Celsius (°C).

`/average`

The average of all readings saved in the database.

`/min-max`

The minimum and maximum values for all sensor readings saved in the database.

`/measurement-info`

The timestamp (UTC) for the first and the latest sensor reading saved in the database along with the number of total readings saved.

`/temperature`

The temperature in degrees Celsius (°C).

`/humidity`

The relative humidity percentage (%).

`/pressure`

The pressure in hectopascal pressure units (hPa).

`/tvoc`

The total volatile organic compounds in parts-per billion (TVOC in ppb).

`/eco2`

CO2 value in parts-per million (ppm).

`/cpu-temp`

The CPU temperature of the Raspberry Pi in degrees Celsius (°C).


## Docker

### Build and run using docker

docker build -t r-api .

docker run –p 80:80 --device /dev/i2c-1 --volume {PWD}/sqlite_db:/sqlite_db r-api

## Links
* BME280 library: https://github.com/pimoroni/bme280-python
* SGP30 library: https://github.com/pimoroni/sgp30-python
* FastAPI: https://fastapi.tiangolo.com
* Humidity conversion formula: https://carnotcycle.wordpress.com/2012/08/04/how-to-convert-relative-humidity-to-absolute-humidity
