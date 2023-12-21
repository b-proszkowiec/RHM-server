FROM balenalib/raspberry-pi-debian

ENV TZ="Europe/Warsaw"
ENV SRV_PORT=50400

WORKDIR /app

COPY src .

RUN apt-get update -y && \
    apt-get update -y  && \
    apt-get autoremove -y && \
    apt-get install gcc-arm-linux-gnueabihf -y && \
    apt-get install build-essential -y	&& \
    apt-get install python3-dev -y

RUN apt-get install python3 -y && \
    apt-get install python3-pip -y && \
    python3 -m pip install --upgrade pip setuptools wheel && \
    pip3 install --root-user-action=ignore requests Adafruit_DHT

EXPOSE $SRV_PORT/udp

CMD ["python3", "measurement.py"]