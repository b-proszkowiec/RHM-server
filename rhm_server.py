#!/usr/bin/python

import socket
import threading
import Adafruit_DHT
from datetime import datetime

localIP     = "0"
localPort   = 50001
bufferSize  = 1024

SENSOR = Adafruit_DHT.AM2302
PIN = '4'


def serverInitialize():

    # Create a datagram socket
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    
    # Bind to address and ip
    UDPServerSocket.bind((localIP, localPort))
    
    print("UDP server up and listening")
    
    # Listen for incoming datagrams
    while(True):
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        client_message = bytesAddressPair[0]
        client_address = bytesAddressPair[1]
    
        if(client_message == b'MEASURE'):
            proc_response = runMeasure()
            if proc_response == 'ERROR':
                continue 
        
            print("proc_response: " + proc_response)
        
            # Sending a reply to client
            UDPServerSocket.sendto(str.encode(proc_response), client_address)

def runMeasure():
    
    queueLock.acquire()
    humidity, temperature = Adafruit_DHT.read_retry(SENSOR, PIN)
    queueLock.release()   
    
    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
    else:
        print('Failed to get reading. Try again!')
        return 'ERROR'
    
    time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    return time + " | " + 'Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity)


queueLock = threading.Lock()

serverInitialize()



