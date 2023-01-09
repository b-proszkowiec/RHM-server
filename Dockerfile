FROM raspbian/stretch

WORKDIR /app

COPY rhm_server.py rhm_server.py

RUN apt-get update -y && \
    apt-get autoremove -y && \
    apt-get install python3 -y && \
    apt-get install python3-pip -y && \
    python3 -m pip install --upgrade pip setuptools wheel && \
    pip3 install Adafruit_DHT

EXPOSE 50400

CMD ["python3", "rhm_server.py"]
