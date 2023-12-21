import socket, os, threading, requests
import schedule, time
import Adafruit_DHT
from rhm_logging import *
from datetime import datetime


localIP     = "0"
localPort   = 50400
bufferSize  = 1024
wait_time = 5       # wait in minutes

api_ip = os.environ.get('API_IP', 'localhost')
api_port = os.environ.get('API_PORT', '6080')
localPort = os.environ.get('SRV_MEAS_PORT', '50401')

SENSOR = Adafruit_DHT.AM2302
PIN = '4'
queueLock = threading.Lock()

def main():
    # Create a thread and run the function
    listening_thread = threading.Thread(target=serverInitialize)
    listening_thread.start()

    schedule.every(wait_time).minutes.do(get_measurement)
    while True:
        schedule.run_pending()
        time.sleep(1)

def serverInitialize():
    # Create a datagram socket
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    
    # Bind to address and ip
    UDPServerSocket.bind((localIP, int(localPort)))
    
    INFO("UDP server up and listening")
    
    # Listen for incoming datagrams
    while(True):
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        client_message = bytesAddressPair[0]
        client_address = bytesAddressPair[1]
    
        if(client_message == b'MEASURE'):
            proc_response = get_measurement()
            if proc_response == None:
                continue 
        
            INFO("proc_response: " + proc_response)
            # Sending a reply to client
            UDPServerSocket.sendto(str.encode(proc_response), client_address)

def runMeasure(queueLock):
    queueLock.acquire()
    humidity, temperature = Adafruit_DHT.read_retry(SENSOR, PIN)
    queueLock.release()

    if humidity is None or temperature is None:
        INFO('Failed to get reading. Try again!')
        return None

    INFO("New measurement prepared: ")
    return  (round(humidity, 1), round(temperature, 1),)

def get_measurement():
    measure_data = runMeasure(queueLock)
    
    if measure_data is not None:
        temperature = measure_data[1]
        humidity = measure_data[0]
        data = {
            "temperature": temperature,
            "humidity": humidity
        }
        try:
            response = requests.post(f'http://{api_ip}:{api_port}/measure', json=data)
            response.raise_for_status()
            INFO("Request was successful. Status: " + str(response.status_code))
        except requests.exceptions.RequestException as e:
            ERROR(f"Error during request to the rest api: {e}")

        time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return time + " | " + 'Temp={}*  Humidity={}%'.format(temperature, humidity)
    
    return measure_data

if __name__ == "__main__":
    main()
