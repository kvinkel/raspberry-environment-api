FROM python:3.7-alpine
RUN pip3 install Flask
RUN pip3 install pimoroni-bme280 smbus2
RUN pip3 install pimoroni-sgp30
RUN mkdir /sqlite_db
COPY ./src .
CMD python3 api.py

