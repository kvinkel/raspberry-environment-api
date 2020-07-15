FROM python:3.7-alpine
RUN pip3 install Flask
RUN pip3 install pimoroni-bme280
COPY ./src .
CMD python3 api.py