# Raspberry Environment aPi

API for monitoring local environment temperature, humidity, pressure, TVOC, and eCO2 on a Raspberry Pi. The sensors used are the BME280 Sensor Breakout and the SGP30 Air Quality Sensor Breakout from Pimoroni. The project aims to provide easy access to current air quality readings and an overview of past readings and tendencies using Python, SQLite, and Docker.

## Docker

### Build and run using docker

docker build -t r-api .

docker run –p 80:80 --device /dev/i2c-1 --volume {PWD}/sqlite_db:/sqlite_db r-api

## Links
* BME280 library: https://github.com/pimoroni/bme280-python
* SGP30 library: https://github.com/pimoroni/sgp30-python
* FastAPI: https://fastapi.tiangolo.com
* Humidity conversion formula: https://carnotcycle.wordpress.com/2012/08/04/how-to-convert-relative-humidity-to-absolute-humidity
