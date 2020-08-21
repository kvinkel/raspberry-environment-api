FROM python:3.8-slim-buster
WORKDIR /usr/src/app
RUN pip3 install fastapi hypercorn
RUN pip3 install pimoroni-bme280 smbus2
RUN pip3 install pimoroni-sgp30
RUN mkdir /sqlite_db
COPY ./src .
CMD hypercorn api:app --bind 0.0.0.0:80
