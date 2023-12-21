import os
from flask import Flask, jsonify, request
from rhm_logging import *
import rhm_service as service

api_port = os.environ.get('API_PORT', '6080')

app = Flask(__name__)

@app.route('/measure', methods=['GET'])
def get_last_measurement():
    meas_data = service.get_last()
    return jsonify(meas_data)

@app.route('/measures', methods=['GET'])
def get_measurements():
    meas_data = service.get_all()
    return jsonify(meas_data)

@app.route('/measure', methods=['POST'])
def save_measurement():
    try:
        data = request.json
        humidity = data['humidity']
        temperature = data['temperature']
        INFO("New measurement arrived: " + str(data))
        service.save_new(temperature, humidity)
    except:
        ERROR("Unable to parse post request data of: " + str(data))
        return {"status": "ERROR"}

    return {"status": "OK"}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=api_port)