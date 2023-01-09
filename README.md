Python DHT22 sensor server
=======================

Read the DHT22 (AM2302) series of humidity and temperature sensors on a Raspberry Pi and enable to reach it over an IP network.


Configuring
----------

Connect your DHT22 humidity sensor to Raspberry PI pins as presented below. Additionally, you can use 10k resistor between Pin 1 and Pin 2 of the DHT22.


![alt text](https://raw.githubusercontent.com/b-proszkowiec/RHM-server/b1a8351235811856026e4b2ff6ad37260d1cd8e5/PI%20DHT22.jpg)

Installing
----------
SSH into a Raspberry Pi and do following.

### 1) Using docker

#### Pull image from dockerhub or build it by your own
````sh
docker pull bproszkowiec/rhm:0.1
````
or

````sh
docker build -t bproszkowiec/rhm .
````

#### Mount volume and run it

````sh
docker run --privileged -d \
  --name=rhm \
  --restart unless-stopped \
  -p 5050:50400/udp \
  bproszkowiec/rhm:0.1
````

### 2) Standard installation

#### Install Adafruit

````sh
sudo apt-get update
sudo apt-get install python3-dev
sudo apt-get install python3-pip
sudo python3 -m pip install --upgrade pip setuptools wheel
sudo pip3 install Adafruit_DHT
````


#### Configure systemd to run server automatically as a service

- edit **rhm.sh** to make sure RHM_PATH variable is set to correct path where **rhm_server.py** is located

- copy **rhm.sh** to **/usr/local/bin** directory
````sh
sudo cp rhm.sh /usr/local/bin
````

- make script executable
````sh
sudo chmod +x /usr/local/bin/rhm.sh
````

- create the Service Unit File
````sh
sudo vim /etc/systemd/system/rhm.service
````

- copy and paste following text
````
[Unit]
Description=Remote Home Manager (RHM)

Wants=network.target
After=syslog.target network-online.target

[Service]
Type=simple
ExecStart=/usr/local/bin/rhm.sh
Restart=on-failure
RestartSec=10
KillMode=process

[Install]
WantedBy=multi-user.target
````

- add read and write permission to the owner
````sh
sudo chmod 640 /etc/systemd/system/rhm.service
````

- enable and start service
````sh
sudo systemctl enable rhm
sudo systemctl start rhm
````

Usage
-----

Download client application for android and see the usage example in rhm-client repository.
